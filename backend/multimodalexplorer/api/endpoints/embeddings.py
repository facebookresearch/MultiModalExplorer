# Copyright (c) Meta Platforms, Inc. and affiliates.

import random
from fastapi import APIRouter

router = APIRouter()


@router.get("/embeddings")
async def get_embeddings():
    batch_size = 700
    num_batches = 100

    embeddings = []
    for _ in range(num_batches):
        batch = [
            [
                -1 + 2 * random.random(),
                -1 + 2 * random.random(),
                round(random.random() * 9),
            ]
            for _ in range(batch_size)
        ]
        embeddings.extend(batch)

    return {"data": embeddings}
