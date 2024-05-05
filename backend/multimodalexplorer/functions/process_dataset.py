# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import csv
import logging
from typing import Any, Dict, List

import torch
from datasets import DatasetDict, load_dataset
from tqdm import tqdm

from multimodalexplorer.types.data_types import DataFileType, DataSetType
from multimodalexplorer.utils.helpers import VALID_DATASET_TYPES_LIST, get_file_path
from multimodalexplorer.utils.utils import load_model, parse_arguments, select_params

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessDataset:
    def __init__(
        self,
        datasets: DataSetType,
        raw_data_file: DataFileType,
        embed_file: DataFileType,
        batch_size: int,
        chunk_size: int,
        dataset_sample_size: int,
    ):
        """
        Initialize ProcessDataset object with necessary attributes.

        Args:
            datasets (list of dict): Types of datasets to process.
                Each dictionary in the list represents a dataset with the following keys:
                    - type (str): Type of the dataset.
                    - name (str): Name of the dataset.
                    - source_lang (str): Source language of the dataset.
            batch_size (int): Batch size for processing data.
            chunk_size (int): Chunk size for saving embeddings to disk.
            raw_data_file/embed_file (list of dict): Dictionary with keys
                - dir (str): Directory/File to save data
                - ext (str): Extension of file
        """

        self.datasets = datasets
        self.batch_size = batch_size
        self.chunk_size = chunk_size
        self.embed_file = embed_file
        self.raw_data_file = raw_data_file
        self.dataset_sample_size = dataset_sample_size

        self.dataset_types, self.dataset_names, self.dataset_src_lang = (
            [item[key] for item in self.datasets]
            for key in ("type", "name", "source_lang")
        )

        self._validate_arguments()

    def _validate_arguments(self) -> None:
        """
        Validate arguments passed during initialization.
        """
        for obj in self.datasets:
            required_keys = {"type", "name", "source_lang"}
            if not required_keys.issubset(obj.keys()):
                raise ValueError(
                    "Dataset Object keys must contain of type, name and source_lang"
                )

        for dtype in self.dataset_types:
            if dtype not in VALID_DATASET_TYPES_LIST:
                raise ValueError(
                    f"Unsupported dataset type: {dtype}. Supported types: {', '.join(VALID_DATASET_TYPES_LIST)}"
                )

    def _extract_data_from_batch(self, batch: Dict[str, Any]) -> List[Any]:
        """
        Extract data from a batch based on its structure.

        Args:
            batch (dict): Batch of data.

        Returns:
            list: Extracted data.
        """
        for key in ["set", "image", "sentence", "audio_url"]:
            if "set" in batch:
                data = [e[0] for e in batch["set"]]
                return [s for s in data if isinstance(s, str) and len(s) <= 514]
            else:
                return [e[key] for e in batch]

        raise ValueError("Unsupported data structure in batch")

    def _save_embeddings(
        self, embeddings_list: List[torch.Tensor], dataset_type: str, file_count: int
    ) -> None:
        """
        Save embeddings to disk.

        Args:
            embeddings_list (list): List of embeddings.
            dataset_type (str): Type of dataset.
            file_count (int): File count for naming the file.
        """
        all_embs = torch.cat(embeddings_list, 0)

        dir_path, ext = self.embed_file.values()
        file_path = get_file_path(
            dir_path, ext, True, f"{dataset_type}_embedding_{file_count}"
        )

        torch.save(all_embs, file_path)

        logger.info(
            f"Saved embeddings for dataset type '{dataset_type}' to {file_path}"
        )

    def _save_data(self, data_list: List[Any], dataset_type: str) -> None:
        """
        Save processed data to disk.

        Args:
            data_list (list): List of processed data.
            dataset_type (str): Type of dataset.
        """
        dir_path, ext = self.raw_data_file.values()
        file_path = get_file_path(dir_path, ext)

        with file_path.open("a+", newline="", encoding="utf-8") as tsvfile:
            fieldnames = ["data", "media_type"]
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter="\t")

            if tsvfile.tell() == 0:
                writer.writeheader()

            for data_row in data_list:
                writer.writerow({"data": data_row, "media_type": dataset_type})

        logger.info(f"Saved data for dataset type '{dataset_type}' to {file_path}")

    def _load_dataset(self) -> Dict[str, Any]:
        """
        Load datasets specified in dataset_names.

        Returns:
            dict: Loaded datasets.
        """
        loaded_datasets = {}

        for dataset_type, dataset_name, dataset_src_lang in zip(
            self.dataset_types, self.dataset_names, self.dataset_src_lang
        ):

            loaded_dataset = load_dataset(dataset_name, split="train")

            loaded_dataset_sample = loaded_dataset.shuffle(seed=42).select(
                range(self.dataset_sample_size)
            )

            logger.info(
                f"Loaded {len(loaded_dataset_sample)} samples from dataset '{dataset_name}'"
            )

            loaded_datasets[dataset_type] = (loaded_dataset_sample, dataset_src_lang)

        return loaded_datasets

    def _embed_dataset(self) -> None:
        """
        Embed datasets.
        """
        loaded_datasets = self._load_dataset()

        for dataset_type, (dataset, dataset_src_lang) in loaded_datasets.items():
            self._process_data(dataset, dataset_type, dataset_src_lang)

    def _process_data(
        self, dataset: DatasetDict, dataset_type: str, dataset_src_lang: str
    ) -> None:
        """
        Process data for a specific dataset type.

        Args:
            dataset_type (str): Type of dataset.
            dataset (datasets.Dataset): Dataset to process.
        """
        data2vec_model = load_model(dataset_type)

        if data2vec_model is None:
            logger.warning(f"No pipeline available for dataset type '{dataset_type}'")
            return

        batch_count = 0
        file_count = 0
        embeddings_list: List[torch.Tensor] = []
        data_list: List[Any] = []

        for batch in tqdm(
            dataset.iter(batch_size=self.batch_size), desc=f"Embedding {dataset_type}"
        ):
            data = self._extract_data_from_batch(batch)

            embeddings = data2vec_model.predict(data, source_lang=dataset_src_lang)

            data_list.extend(data)
            embeddings_list.append(embeddings)

            batch_count += self.batch_size

            if batch_count >= self.chunk_size:
                self._save_embeddings(embeddings_list, dataset_type, file_count)
                self._save_data(data_list, dataset_type)

                embeddings_list = []
                data_list = []
                batch_count = 0
                file_count += 1

        if embeddings_list:
            self._save_embeddings(embeddings_list, dataset_type, file_count)
            self._save_data(data_list, dataset_type)

    def process(self) -> None:
        """
        Process all datasets.
        """
        try:
            self._embed_dataset()
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    p_list = [
        "datasets",
        "raw_data_file",
        "embed_file",
        "batch_size",
        "chunk_size",
        "dataset_sample_size",
    ]
    args = parse_arguments()
    params = select_params(args, p_list)

    logger.info("Arguments: %s", params)

    processer = ProcessDataset(*params)
    processer.process()
