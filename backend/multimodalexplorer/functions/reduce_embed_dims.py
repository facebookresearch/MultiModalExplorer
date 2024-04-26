# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from typing import Any, Dict

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from umap import UMAP

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


class ReduceEmbedDims:
    def __init__(
        self,
        embed_file: DataFileType,
        umap_file: DataFileType,
        umap_args: Dict[str, Any],
        kmean_args: Dict[str, Any],
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
        self.kmean_args = kmean_args

    def _cluster_embed(self, embeddings):
        """
        Cluster embeddings using K-Means.

        Args:
            embeddings (numpy.ndarray): Input embeddings.

        Returns:
            numpy.ndarray: Embeddings with additional cluster labels.
        """
        # Create K-Means model
        n_clusters, n_init, random_state = self.kmean_args.values()
        kmeans = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=random_state)

        # Perform clustering
        clusters = kmeans.fit_predict(embeddings)

        # Append cluster labels to embeddings
        embedding_with_clusters = np.column_stack((embeddings, clusters))

        return embedding_with_clusters

    def _normalize_embed(self, umap_embeddings):
        """
        Normalize embeddings and cluster them.

        Args:
            umap_embeddings (numpy.ndarray): UMAP embeddings.

        Returns:
            numpy.ndarray: Normalized embeddings with clusters.
        """
        # Normalize embeddings to [-1, 1] range
        scaler = MinMaxScaler(feature_range=(-1, 1))
        normalized_embeddings = scaler.fit_transform(umap_embeddings)

        # Cluster normalized embeddings
        return self._cluster_embed(normalized_embeddings)

    def _reduce_dims(self) -> None:
        """
        Reduce the dimensions of embeddings using UMAP.
        """
        embeddings = concat_embed_from_dir(self.embed_file["dir"])

        umap_model = UMAP(**self.umap_args)
        umap_embeddings = umap_model.fit_transform(embeddings)

        normailize_umap_embedding = self._normalize_embed(umap_embeddings)

        dir_path, ext = self.umap_file.values()
        file_path = get_file_path(dir_path, ext)

        with open(file_path, "wb") as file:
            np.save(file, normailize_umap_embedding)

        logger.info(
            f"Created UMAP embeddings for {len(normailize_umap_embedding)} samples."
        )

    def process(self) -> None:
        """
        Process the reduction of embeddings to UMAP space and handle exceptions.
        """
        try:
            self._reduce_dims()
        except Exception as e:
            logger.exception(f"An error occurred during dimension reduction: {e}")


if __name__ == "__main__":
    p_list = ["embed_file", "umap_file", "umap_args", "kmean_args"]
    args = parse_arguments()
    params = select_params(args, p_list)

    logger.info("Arguments: %s", params)

    processor = ReduceEmbedDims(*params)
    processor.process()
