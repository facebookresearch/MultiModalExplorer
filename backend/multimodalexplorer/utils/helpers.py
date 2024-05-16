# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from enum import Enum
from pathlib import Path
from typing import Optional

import torch

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

VALID_DATASET_TYPES = ("text", "image", "audio", "video")

VALID_DATASET_TYPES_LIST = list(VALID_DATASET_TYPES)

DatasetType = Enum("DatasetType", VALID_DATASET_TYPES)


def get_file_path(
    dir_name: str,
    extension: str,
    is_write: bool = True,
    file_name: Optional[str] = None,
) -> Path:
    folder_path = Path(dir_name).absolute()

    if file_name is None:
        file_name = folder_path.name

    file_name_with_extension = f"{file_name}.{extension}"

    file_path = folder_path / file_name_with_extension

    # Disallow from creating parent folders/files if it is not write access
    if is_write == True:
        folder_path.mkdir(parents=True, exist_ok=True)
    else:
        # raise FileNotFoundError error if is_write is False and file_path does not exist
        if not file_path.exists():
            raise FileNotFoundError(f"File Path '{file_path}' not found.")

    return file_path
