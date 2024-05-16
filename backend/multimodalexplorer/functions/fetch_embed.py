# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging
from typing import Any, Dict, List, Optional

import numpy as np

from multimodalexplorer.utils.helpers import get_file_path
from multimodalexplorer.utils.utils import (
    get_embeds_details,
    parse_arguments,
    select_params,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse command line arguments
args = parse_arguments()

# Select relevant parameters
params = select_params(args, ["umap_file", "raw_data_file"])
umap_file, raw_data_file = params


def fetch_embeds() -> list:
    """
    Load UMAP embeddings from the stored file.

    Returns:
        np.ndarray or None: The loaded UMAP embeddings or None if an error occurred.
    """
    dir_path, ext = umap_file.values()
    file_path = get_file_path(dir_path, ext, False)

    with open(file_path, "rb") as file:
        embeddings = np.load(file)

    embeddings_list = embeddings.tolist()

    logger.info(f"Loaded UMAP embeddings with shape: {len(embeddings_list)}")
    return embeddings_list


def fetch_embeds_details(pointList: List) -> Optional[List[Dict[str, Any]]]:
    results = get_embeds_details(pointList, raw_data_file)

    return results
