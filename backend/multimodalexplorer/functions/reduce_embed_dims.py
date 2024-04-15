# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
import pickle

from umap import UMAP

from .helpers import get_file_path, load_embeddings_from_files

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReduceEmbedDims:
    def __init__(self, umap_dirname="umap_embeddings", embedding_dirname="embeddings"):
        self.umap_dirname = umap_dirname
        self.embedding_dirname = embedding_dirname

    def _get_emb_path(self):
        """
        Get the file path for storing UMAP embeddings.
        """
        file_name = f"{self.umap_dirname}.pickle"
        file_path = get_file_path(file_name, f"../{self.umap_dirname}")
        return file_path

    def _reduce_dims(self):
        """
        Reduce the dimensions of embeddings using UMAP.
        """
        embeddings = load_embeddings_from_files(self.embedding_dirname)

        # Create UMAP object to reduce dataset dimensions
        umap_model = UMAP(n_neighbors=15, n_components=2, min_dist=0.1)
        embeddings_umap = umap_model.fit_transform(embeddings)

        file_path = self._get_emb_path()

        with open(file_path, "wb") as file:
            pickle.dump(embeddings_umap, file)
        logger.info(f"Created UMAP embeddings for {len(embeddings_umap)} samples.")

    def load_embeddings(self):
        """
        Load UMAP embeddings from the stored file.
        """
        file_path = self._get_emb_path()

        try:
            with open(file_path, "rb") as file:
                embeddings = pickle.load(file)
                logger.info(f"Loaded UMAP embeddings with shape: {embeddings.shape}")
                return embeddings
        except FileNotFoundError:
            logger.error(f"UMAP embeddings file not found at: {file_path}")
            return None
        except Exception as e:
            logger.exception(f"An error occurred while loading UMAP embeddings: {e}")
            return None

    def process(self):
        """
        Process the reduction of embeddings to UMAP space and handle exceptions.
        """
        try:
            self._reduce_dims()
        except Exception as e:
            logger.exception(f"An error occurred during dimension reduction: {e}")


if __name__ == "__main__":
    # Entry point of the script
    processor = ReduceEmbedDims()
    processor.process()
