# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


from typing import List

from pydantic import BaseModel, Field


class EmbeddingData(BaseModel):
    index: int
    media_type: str
    data: str


# get_embeddings route
class EmbeddingsResponse(BaseModel):
    data: List[List[float]]


# get_embedding_details route
class EmbeddingsDetailsRequest(BaseModel):
    points: List[int] = Field(..., description="list of points")


class EmbeddingsDetailsResponse(BaseModel):
    data: List[EmbeddingData]


# get_search route
class SearchRequest(BaseModel):
    search_data: str
    search_type: str
    search_src_lang: str = "eng_Latn"


class SearchResponse(BaseModel):
    data: List[EmbeddingData]
