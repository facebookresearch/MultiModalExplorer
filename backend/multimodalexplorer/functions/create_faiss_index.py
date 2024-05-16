# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging

import faiss
import numpy as np
import torch

from multimodalexplorer.types.data_types import DataFileType
from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import (
    concat_embed_from_dir,
    parse_arguments,
    select_params,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateFaissIndex:
    def __init__(
        self,
        embed_file: DataFileType,
        index_file: DataFileType,
        train_data_size: int,
    ):
        """
        Initialize CreateFaissIndex class with directory and filename parameters.

        Args:
            embed_file (DataFileType): Directory and filename for input embeddings.
            index_file (DataFileType): Directory and filename for output index.
            train_data_size (int): Size of the random subset used for training the index.
        """
        self.embed_file = embed_file
        self.index_file = index_file
        self.train_data_size = train_data_size

    def _create_index(self):
        """
        Create Faiss index using OPQ64, IVF1024, and PQ64 methods.
        """
        # Concatenate embeddings from directory
        embeddings = concat_embed_from_dir(self.embed_file["dir"])
        vector_dims = embeddings.shape[1]

        # Create Faiss index with OPQ64, IVF1024, and PQ64 methods
        index = faiss.index_factory(vector_dims, "OPQ64,IVF1024,PQ64")

        # Move index to GPU if available
        if torch.cuda.is_available():
            co = faiss.GpuMultipleClonerOptions()
            co.useFloat16 = True
            index = faiss.index_cpu_to_all_gpus(index, co=co)

        # Convert embeddings to numpy array and normalize them
        if torch.cuda.is_available():
            data = embeddings.detach().cpu().numpy().astype(np.float32)
        else:
            data = embeddings.numpy().astype(np.float32)
        faiss.normalize_L2(data)

        # Get random subset without replacement for training the index
        random_data_subset = embeddings[
            np.random.choice(
                embeddings.shape[0], size=self.train_data_size, replace=False
            ),
            :,
        ]

        # Train the index with the random subset
        index.train(random_data_subset)
        logger.info(
            f"Training index with random subset of data - {len(random_data_subset)}"
        )

        # Add all data to the index
        index.add(data)
        logger.info("Adding data to index")

        # Get file path for saving the index
        dir_path, ext = self.index_file.values()
        file_path = get_file_path(dir_path, ext)

        # Write index to file
        faiss.write_index(index, str(file_path))
        logger.info(f"Created Faiss index for embeddings - {index.ntotal}")

    def process(self):
        """
        Process method to create Faiss index with error handling.
        """
        try:
            self._create_index()
        except Exception as e:
            logger.exception("Could not create faiss index", exc_info=e)
            return None


if __name__ == "__main__":
    p_list = ["embed_file", "index_file", "train_data_size"]
    args = parse_arguments()
    params = select_params(args, p_list)

    logger.info("Arguments: %s", params)

    processer = CreateFaissIndex(*params)
    processer.process()
