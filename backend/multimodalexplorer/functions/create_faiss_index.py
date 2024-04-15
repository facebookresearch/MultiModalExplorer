# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging

import faiss
import numpy as np
import torch

from .helpers import get_file_path, index_to_gpu, load_embeddings_from_files

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the device (CPU or GPU) for torch operations
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class CreateFaissIndex:
    def __init__(
        self,
        load_embedding_dirname="embeddings",
        save_index_dirname="db",
        save_index_filename="faiss_index",
        train_data_size=300,
    ):
        """
        Initialize CreateFaissIndex class with directory and filename parameters.
        """
        self.load_embedding_dirname = load_embedding_dirname
        self.save_index_dirname = save_index_dirname
        self.save_index_filename = save_index_filename
        self.train_data_size = train_data_size

    def create_index(self):
        """
        Create Faiss index using OPQ64, IVF1024, and PQ64 methods.
        """

        embeddings = load_embeddings_from_files(self.load_embedding_dirname)
        vector_dims = embeddings.shape[1]

        index = faiss.index_factory(vector_dims, "OPQ64,IVF1024,PQ64")

        if DEVICE == "gpu":
            index = index_to_gpu(index, faiss)

        if DEVICE == "gpu":
            data = embeddings.detach().cpu().numpy().astype(np.float32)
        else:
            data = embeddings.numpy().astype(np.float32)

        faiss.normalize_L2(data)

        # Get random subset without replacement
        random_data_subset = np.random.choice(
            data, size=self.train_data_size, replace=False
        )
        index.train(random_data_subset)

        index.add(data)

        file_name = f"{self.save_index_filename}.bin"
        file_path = get_file_path(file_name, f"../{self.save_index_dirname}")

        faiss.write_index(index, file_path)
        logger.info(f"Created Faiss index for embeddings - {index.ntotal}")

    def process(self):
        """
        Process method to create Faiss index with error handling.
        """
        try:
            self.create_index()
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return None


if __name__ == "__main__":
    processer = CreateFaissIndex()
    processer.process()
