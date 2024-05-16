# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


from typing import TypedDict


class DataFileType(TypedDict):
    dir: str
    ext: str


class DataSetType(TypedDict):
    type: str
    name: str
    source_lang: str


class EmbeddingDataType(TypedDict):
    index: int
    media_type: str
    data: str
