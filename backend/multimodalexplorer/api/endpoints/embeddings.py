# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import random

from fastapi import APIRouter

from ...functions.reduce_embed_dims import ReduceEmbedDims

router = APIRouter()

reduce_embs = ReduceEmbedDims()


@router.get("/embeddings")
async def get_embeddings():
    embeddings = reduce_embs.load_embeddings().tolist()

    return {"data": embeddings}
