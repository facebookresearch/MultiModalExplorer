# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
from typing import Any, Dict, Optional

import numpy as np
from multimodalexplorer.types.data_types import DataFileType
from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import (
    concat_embed_from_dir,
    load_config,
    parse_arguments,
)
from umap import UMAP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReduceEmbedDims:
    def __init__(
        self,
        embed_file: DataFileType,
        umap_file: DataFileType,
        umap_args: Dict[str, Any],
    ):
        """
        Initialize the ReduceEmbedDims class.

        Args:
            embed_file (DataFileType): A dictionary containing the directory and extension for the embeddings file.
            umap_file (DataFileType): A dictionary containing the directory and extension for the UMAP embeddings file.
            umap_args (Dict[str, Any]): A dictionary containing the arguments for the UMAP model.
        """
        self.embed_file = embed_file
        self.umap_file = umap_file
        self.umap_args = umap_args

    def load_embeddings(self) -> Optional[np.ndarray]:
        """
        Load UMAP embeddings from the stored file.

        Returns:
            np.ndarray or None: The loaded UMAP embeddings or None if an error occurred.
        """
        dir_path, ext = self.umap_file.values()
        file_path = get_file_path(dir_path, ext)

        try:
            with open(file_path, "rb") as file:
                embeddings = np.load(file)
            logger.info(f"Loaded UMAP embeddings with shape: {embeddings.shape}")
            return embeddings
        except FileNotFoundError:
            logger.error(f"UMAP embeddings file not found at: {file_path}")
            return None
        except Exception as e:
            logger.exception(f"An error occurred while loading UMAP embeddings: {e}")
            return None

    def _reduce_dims(self) -> None:
        """
        Reduce the dimensions of embeddings using UMAP.
        """
        embeddings = concat_embed_from_dir(self.embed_file["dir"])
        umap_model = UMAP(**self.umap_args)
        umap_embeddings = umap_model.fit_transform(embeddings)

        dir_path, ext = self.umap_file.values()
        file_path = get_file_path(dir_path, ext)

        with open(file_path, "wb") as file:
            np.save(file, umap_embeddings)

        logger.info(f"Created UMAP embeddings for {len(umap_embeddings)} samples.")

    def process(self) -> None:
        """
        Process the reduction of embeddings to UMAP space and handle exceptions.
        """
        try:
            self._reduce_dims()
        except Exception as e:
            logger.exception(f"An error occurred during dimension reduction: {e}")


if __name__ == "__main__":
    p_list = ["embed_file", "umap_file", "umap_args"]
    args = parse_arguments(p_list)
    params = load_config(args.config, p_list)

    logger.info("Arguments: %s", params)

    processor = ReduceEmbedDims(*params)
    processor.process()
