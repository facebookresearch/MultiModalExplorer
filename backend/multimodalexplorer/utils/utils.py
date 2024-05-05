# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pyarrow as pa
import pyarrow.csv as pa_csv
import torch
from sonar.inference_pipelines.speech import SpeechToEmbeddingModelPipeline
from sonar.inference_pipelines.text import TextToEmbeddingModelPipeline

from multimodalexplorer.types.data_types import DataFileType, EmbeddingDataType
from multimodalexplorer.utils.helpers import DEVICE, VALID_DATASET_TYPES, get_file_path

LOADED_MODELS: Dict[str, Any] = {}

LOADED_DATA: pa.Table = None


def load_model(dataset_type: str) -> Any:
    """
    Load the model for a specific dataset type.

    Args:
        dataset_type (str): Type of dataset.
        device (Any): Device to load the model on.

    Returns:
        Any: Loaded model pipeline.
    """
    if dataset_type not in VALID_DATASET_TYPES:
        raise ValueError(
            f"Unsupported dataset type: {dataset_type}. Supported types: {', '.join(VALID_DATASET_TYPES)}"
        )

    if dataset_type in LOADED_MODELS:
        return LOADED_MODELS[dataset_type]

    if dataset_type == "text":
        model = TextToEmbeddingModelPipeline(
            encoder="text_sonar_basic_encoder",
            tokenizer="text_sonar_basic_encoder",
            device=DEVICE,
        )
    elif dataset_type == "audio":
        model = SpeechToEmbeddingModelPipeline(
            encoder="sonar_speech_encoder_eng", device=DEVICE
        )
    else:
        model = None

    if model is not None:
        LOADED_MODELS[dataset_type] = model

    return model


def load_raw_data(raw_data_file) -> pa.Table:
    global LOADED_DATA
    if LOADED_DATA is None:
        dir_path, ext = raw_data_file.values()
        file_path = get_file_path(dir_path, ext, False)

        LOADED_DATA = pa_csv.read_csv(
            file_path, parse_options=pa.csv.ParseOptions(delimiter="\t")
        )
    return LOADED_DATA


def select_params(
    config: Dict[str, Any], key_list: List[str]
) -> List[Union[str, int, Dict]]:
    picked_config = {key: config[key] for key in key_list if key in config}

    params = list(picked_config.values())

    return params


def parse_arguments() -> Dict[str, Union[str, int, Dict]]:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=str,
        help=f"Path to the configuration file. The configuration file should be a JSON file containing settings for the script. Default value is 'config.json'.",
        default="config.json",
    )

    args = parser.parse_args()

    config_file_path = Path(args.config).absolute()
    with open(config_file_path, "r") as f:
        config = json.load(f)

    return config


def concat_embed_from_dir(dirname: str) -> torch.Tensor:
    embeddings_list: List[torch.Tensor] = []

    folder_path: Path = Path(dirname).absolute()

    # Sort files according to their order in the folder
    files: List[Path] = sorted(folder_path.iterdir(), key=lambda x: x.stat().st_mtime)

    for file_path in files:
        if file_path.is_file():
            embeddings: torch.Tensor = torch.load(file_path)
            embeddings_list.append(embeddings)

    return torch.cat(embeddings_list, dim=0)


def get_embeds_details(
    list: List, raw_data_file: DataFileType
) -> Optional[List[EmbeddingDataType]]:

    data_table = load_raw_data(raw_data_file)
    results = []

    for idx in list:
        row = data_table.slice(idx, 1).to_pydict()
        obj = {
            "index": idx,
            "data": row["data"][0],
            "media_type": row["media_type"][0],
        }
        results.append(obj)

    return results
