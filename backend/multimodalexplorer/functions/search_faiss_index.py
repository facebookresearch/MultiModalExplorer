# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
import os
from typing import List

import faiss
import numpy as np

from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import (
    get_embeds_details,
    load_model,
    parse_arguments,
    select_params,
)

# Set KMP_DUPLICATE_LIB_OK environment variable to TRUE
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Parse command line arguments
args = parse_arguments()
params = select_params(args, ["index_file", "raw_data_file", "index_args"])
index_file, raw_data_file, index_args = params


class SearchFaissIndex:
    def __init__(
        self,
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
        self.table = None

    def _load_index(self) -> faiss.Index:
        """
        Load the Faiss index.

        Returns:
            faiss.Index: Loaded Faiss index.
        """
        dir_path, ext = self.index_file.values()
        file_path = get_file_path(dir_path, ext, False)

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
        search_data, search_type, search_src_lang = search_query.values()

        data2vec_model = load_model(search_type)

        if data2vec_model is None:
            logger.warning(f"No pipeline available for dataset type '{search_type}'")
            return

        query_embedding = data2vec_model.predict(
            [search_data], source_lang=search_src_lang
        )

        return query_embedding.numpy().astype(np.float32)

    def _query_index(self, search_query: dict) -> List[List[int]]:
        """
        Search the Faiss index using the query and return results.

        Args:
            search_query (dict): Search query.

        Returns:
            list: List of indices.
        """
        index = self._load_index()

        query_embedding = self._process_search_query(search_query)
        faiss.normalize_L2(query_embedding)

        _, indices = index.search(query_embedding, self.index_args["k_neighbors"])

        return indices

    def _search_results(self, indices) -> list:
        """
        Search the Faiss index using the query and return results.

        Args:
            indices (list): Indices from faiss-index search.

        Returns:
            list: List of search results.
        """
        idxs = indices[0]
        results = get_embeds_details(idxs, self.raw_data_file)

        return results

    def process(self, search_query: dict) -> None:
        """
        Process the search on faiss index and handle exceptions.
        """
        try:
            indices = self._query_index(search_query)
            return self._search_results(indices)
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            raise e
