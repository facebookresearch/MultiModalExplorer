# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import parse_arguments, select_params

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_embed() -> Optional[List[Dict[str, Any]]]:
    """
    Load UMAP embeddings from the stored file and merge them with raw data.

    Returns:
        Optional[List[Dict[str, Any]]]: The merged data containing UMAP embeddings or None if an error occurred.
    """
    # Parse command line arguments
    args = parse_arguments()
    # Select relevant parameters
    params = select_params(args, ["umap_file", "raw_data_file"])
    umap_file, raw_data_file = params

    # Get file paths for UMAP embeddings and raw data
    dir_path, ext = umap_file.values()
    file_path_embed = get_file_path(dir_path, ext)

    dir_path, ext = raw_data_file.values()
    file_path_raw = get_file_path(dir_path, ext)

    try:
        # Load raw data
        raw_data = pd.read_csv(file_path_raw, sep="\t")

        # Load UMAP embeddings
        with open(file_path_embed, "rb") as file:
            embeddings = np.load(file)

        # Merge raw data with UMAP embeddings
        merged_data = pd.concat([raw_data, pd.DataFrame(embeddings)], axis=1)

        # Rename columns
        merged_data.rename(
            columns={
                merged_data.columns[-3]: "x",
                merged_data.columns[-2]: "y",
                merged_data.columns[-1]: "cluster",
            },
            inplace=True,
        )

        # Convert merged data to list of dictionary records
        merged_embed_data = merged_data.to_dict("records")

        logger.info(f"Loaded UMAP embeddings with shape: {embeddings.shape}")

        return merged_embed_data
    except FileNotFoundError:
        logger.error(f"UMAP embeddings file not found at: {file_path_embed}")
        return None
    except Exception as e:
        logger.exception(f"An error occurred while loading UMAP embeddings: {e}")
        return None
