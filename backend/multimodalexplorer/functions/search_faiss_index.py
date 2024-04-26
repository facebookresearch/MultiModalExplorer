# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
import os
from typing import List

import faiss
import numpy as np
import pandas as pd

from multimodalexplorer.types.data_types import DataFileType
from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import load_model

# Set KMP_DUPLICATE_LIB_OK environment variable to TRUE
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchFaissIndex:
    def __init__(
        self, index_file: DataFileType, raw_data_file: DataFileType, index_args: dict
    ):
        """
        Initialize SearchFaissIndex object.

        Args:
            index_file (DataFileType): File path and extension of the Faiss index.
            raw_data_file (DataFileType): File path and extension of the raw data.
            index_args (dict): Arguments for searching the Faiss index.
        """
        self.index_file = index_file
        self.raw_data_file = raw_data_file
        self.index_args = index_args

    def _load_index(self) -> faiss.Index:
        """
        Load the Faiss index.

        Returns:
            faiss.Index: Loaded Faiss index.
        """
        dir_path, ext = self.index_file.values()
        file_path = get_file_path(dir_path, ext)

        if not file_path.exists():
            raise FileNotFoundError(f"Index file '{file_path}' not found.")

        index = faiss.read_index(str(file_path))
        return index

    def _process_search_query(self, search_query: dict) -> np.ndarray:
        """
        Process the search query and generate embeddings.

        Args:
            search_query (dict): Search query containing search data, type, and source language.

        Returns:
            np.ndarray: Query embeddings.
        """
        if not search_query:
            raise ValueError("Search data is empty.")

        required_keys = {"search_data", "search_type", "search_src_lang"}
        if not required_keys.issubset(search_query.keys()):
            raise ValueError(
                "Search object keys must contain 'search_data', 'search_type', and 'search_src_lang'"
            )

        search_data, search_type, search_src_lang = search_query.values()

        data2vec_model = load_model(search_type)

        if data2vec_model is None:
            logger.warning(f"No pipeline available for dataset type '{search_type}'")
            return

        query_embedding = data2vec_model.predict(
            [search_data], source_lang=search_src_lang
        )

        return query_embedding.numpy().astype(np.float32)

    def _query_result(self, indices) -> list:

        if len(indices) == 0:
            return []

        dir_path, ext = self.raw_data_file.values()
        file_path = get_file_path(dir_path, ext)

        raw_data = pd.read_csv(file_path, sep="\t")

        search_results = []
        node_idxs = indices[0]

        for idx in node_idxs:
            row = raw_data.iloc[idx]
            obj = {
                "index": str(idx),
                "data": row["data"],
                "media_type": row["media_type"],
            }
            search_results.append(obj)

        return search_results

    def _query_index(self, search_query: dict) -> List[List[int]]:
        """
        Search the Faiss index using the query and return results.

        Args:
            search_query (dict): Search query.

        Returns:
            list: List of search results.
        """
        index = self._load_index()

        query_embedding = self._process_search_query(search_query)
        faiss.normalize_L2(query_embedding)

        _, indices = index.search(query_embedding, self.index_args["k_neighbors"])

        return self._query_result(indices)

    def process(self, search_query: dict) -> None:
        """
        Process the search on faiss index and handle exceptions.
        """
        try:
            return self._query_index(search_query)
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return None
