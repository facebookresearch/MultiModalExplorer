# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import argparse
import csv
import logging

import torch
from datasets import load_dataset
from sonar.inference_pipelines.speech import SpeechToEmbeddingModelPipeline
from sonar.inference_pipelines.text import TextToEmbeddingModelPipeline
from tqdm import tqdm

from .helpers import get_file_path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the device (CPU or GPU) for torch operations
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class ProcessDataset:
    def __init__(
        self,
        dataset_types,
        dataset_names,
        batch_size,
        chunk_size,
        embed_save_dir_name="embeddings",
        data_save_dir_name="data",
    ):
        """
        Initialize ProcessDataset object with necessary attributes.

        Args:
            dataset_types (list of str): Types of datasets to process.
            dataset_names (list of str): Names of datasets to load.
            batch_size (int): Batch size for processing data.
            chunk_size (int): Chunk size for saving embeddings to disk.
            embed_save_dir_name (str, optional): Name of directory to save embeddings. Defaults to "embeddings".
            data_save_dir_name (str, optional): Name of directory to save processed data. Defaults to "data".
        """
        self.dataset_types = dataset_types
        self.dataset_names = dataset_names
        self.batch_size = batch_size
        self.chunk_size = chunk_size
        self.embed_save_dir_name = embed_save_dir_name
        self.data_save_dir_name = data_save_dir_name
        self.device = DEVICE

        self._validate_arguments()

    def _validate_arguments(self):
        """
        Validate arguments passed during initialization.
        """
        if len(self.dataset_types) != len(self.dataset_names):
            raise ValueError(
                "Lengths of dataset_types and dataset_names must be equal."
            )

        valid_types = ["text", "image", "audio", "video"]
        for dtype in self.dataset_types:
            if dtype not in valid_types:
                raise ValueError(
                    f"Unsupported dataset type: {dtype}. Supported types: {', '.join(valid_types)}"
                )

    def _extract_data_from_batch(self, batch):
        """
        Extract data from a batch based on its structure.

        Args:
            batch (dict): Batch of data.

        Returns:
            list: Extracted data.
        """
        for key in ["set", "image", "sentence", "audio_url"]:
            if key in batch:
                return [e[key] for e in batch]

        raise ValueError("Unsupported data structure in batch")

    def _load_dataset(self):
        """
        Load datasets specified in dataset_names.

        Returns:
            dict: Loaded datasets.
        """
        loaded_datasets = {}

        for dataset_type, dataset_name in zip(self.dataset_types, self.dataset_names):
            loaded_dataset = load_dataset(dataset_name, split="train")

            logger.info(
                f"Loaded {len(loaded_dataset)} samples from dataset '{dataset_name}'"
            )

            loaded_datasets[dataset_type] = loaded_dataset

        return loaded_datasets

    def _save_embeddings(self, embeddings_list, dataset_type, file_count):
        """
        Save embeddings to disk.

        Args:
            embeddings_list (list): List of embeddings.
            dataset_type (str): Type of dataset.
            file_count (int): File count for naming the file.
        """
        all_embs = torch.cat(embeddings_list, 0)

        file_name = f"{dataset_type}_{self.embed_save_dir_name}_{file_count}.pt"
        file_path = get_file_path(file_name, f"../{self.embed_save_dir_name}")

        torch.save(all_embs, file_path)

        logger.info(
            f"Saved embeddings for dataset type '{dataset_type}' to {file_path}"
        )

    def _save_data(self, data_list, dataset_type):
        """
        Save processed data to disk.

        Args:
            data_list (list): List of processed data.
            dataset_type (str): Type of dataset.
        """
        file_name = f"{self.data_save_dir_name}_chunk.tsv"
        file_path = get_file_path(file_name, f"../{self.data_save_dir_name}")

        with open(file_path, "a+", newline="", encoding="utf-8") as tsvfile:
            fieldnames = ["data", "media_type"]
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter="\t")

            if tsvfile.tell() == 0:
                writer.writeheader()

            for data_row in data_list:
                writer.writerow({"data": data_row, "media_type": dataset_type})

        logger.info(f"Saved data for dataset type '{dataset_type}' to {file_path}")

    def _process_data(self, dataset_type, dataset):
        """
        Process data for a specific dataset type.

        Args:
            dataset_type (str): Type of dataset.
            dataset (datasets.Dataset): Dataset to process.
        """
        data2vec_model = {
            "text": TextToEmbeddingModelPipeline(
                encoder="text_sonar_basic_encoder",
                tokenizer="text_sonar_basic_encoder",
                device=self.device,
            ),
            "audio": SpeechToEmbeddingModelPipeline(
                encoder="sonar_speech_encoder_eng", device=self.device
            ),
        }[dataset_type]

        batch_count = 0
        file_count = 0
        embeddings_list = []
        data_list = []

        for batch in tqdm(
            dataset.iter(batch_size=self.batch_size), desc=f"Embedding {dataset_type}"
        ):
            data = self._extract_data_from_batch(batch)
            embeddings = data2vec_model.predict(data, source_lang="eng_Latn")

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

    def _embed_dataset(self):
        """
        Embed datasets.
        """
        loaded_datasets = self._load_dataset()

        for dataset_type, dataset in loaded_datasets.items():
            self._process_data(dataset_type, dataset)

    def process(self):
        """
        Process all datasets.
        """
        try:
            self._embed_dataset()
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return None


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset_types",
        nargs="+",
        type=str,
        help="Types of the dataset",
        default=["text"],
    )
    parser.add_argument(
        "--dataset_names",
        nargs="+",
        type=str,
        help="Names of the dataset",
        default=["embedding-data/sentence-compression"],
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        help="Batch Size to be used to generate embeddings",
        default=50,
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        help="Chunk Size to be used to save embeddings to disk",
        default=100,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logger.info("Arguments: %s", args)

    processer = ProcessDataset(
        args.dataset_types, args.dataset_names, args.batch_size, args.chunk_size
    )
    processer.process()
