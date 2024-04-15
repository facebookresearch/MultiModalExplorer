# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import logging
import os

import faiss
import numpy as np
import pandas as pd
import torch
from sonar.inference_pipelines.speech import SpeechToEmbeddingModelPipeline
from sonar.inference_pipelines.text import TextToEmbeddingModelPipeline

from .helpers import get_file_path

# Set environment variable to avoid OpenMP runtime issues
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the device (CPU or GPU) for torch operations
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class SearchFaissIndex:
    def __init__(
        self,
        search_data,
        search_data_type,
        index_filename="faiss_index",
        data_filename="data",
    ):
        """
        Initialize SearchFaissIndex instance.

        Args:
            search_data (str): The data to be searched.
            search_data_type (str): Type of search data, e.g., 'text', 'image'.
            index_filename (str): Filename of the Faiss index.
        """
        # Initialize class attributes
        self.search_data = search_data
        self.search_data_type = search_data_type
        self.index_filename = index_filename
        self.data_filename = data_filename
        self.device = DEVICE

        # Validate arguments
        self._validate_arguments()

    def _validate_arguments(self):
        """
        Validate the provided arguments.
        """
        # Ensure dataset types are valid
        valid_types = ["text", "image", "audio", "video"]
        if self.search_data_type not in valid_types:
            raise ValueError(
                f"Unsupported dataset type: {self.search_data_type}. Supported types: {', '.join(valid_types)}"
            )

    def _load_index_from_file(self):
        """
        Load the Faiss index from file.

        Returns:
            faiss.Index: Loaded Faiss index.
        """
        file_name = f"{self.index_filename}.bin"
        file_path = get_file_path(file_name, f"../db")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Index file '{file_path}' not found.")

        index = faiss.read_index(file_path)
        return index

    def process_search_query(self):
        """
        Process the search query and obtain its embedding.

        Returns:
            np.ndarray: Query_embedding as a NumPy array.
        """

        if not self.search_data:
            raise ValueError("Search data is empty.")

        data2vec_model = {
            "text": TextToEmbeddingModelPipeline(
                encoder="text_sonar_basic_encoder",
                tokenizer="text_sonar_basic_encoder",
                device=self.device,
            ),
            "audio": SpeechToEmbeddingModelPipeline(
                encoder="sonar_speech_encoder_eng", device=self.device
            ),
        }[self.search_data_type]

        if data2vec_model is None:
            raise ValueError(f"No model found for data type: {self.search_data_type}")

        query_embedding = data2vec_model.predict(
            [self.search_data], source_lang="eng_Latn"
        )

        return query_embedding.numpy().astype(np.float32)

    def search_index(self):
        """
        Search the Faiss index with the query embedding.

        Returns:
            tuple: Two arrays containing distances and indices of nearest neighbors.
        """
        index = self._load_index_from_file()

        query_embedding = self.process_search_query()
        k = 5

        faiss.normalize_L2(query_embedding)
        D, I = index.search(query_embedding, k)

        file_name = f"{self.data_filename}_chunk.tsv"
        file_path = get_file_path(file_name, f"../{self.data_filename}")

        raw_data = pd.read_csv(file_path, sep="\t")

        list_searches = [raw_data.iloc[idx]["data"] for idx in I]
        return list_searches

    def process(self):
        """
        Process the search query and handle exceptions.
        """
        try:
            list_searches = self.search_index()
            print(list_searches)
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return None


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser()

    # Add arguments with default values
    parser.add_argument(
        "--search_data",
        help="Provide search query data files for - text, image, audio",
        default="Asian stock markets",
    )
    parser.add_argument(
        "--search_data_type",
        type=str,
        help="Provide search query data type - text, image, audio",
        default="text",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # Entry point of the script
    args = parse_arguments()  # Parse arguments
    logger.info("Arguments: %s", args)  # Log parsed arguments

    processor = SearchFaissIndex(args.search_data, args.search_data_type)
    processor.process()
