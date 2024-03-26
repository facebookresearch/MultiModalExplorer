# Copyright (c) Meta Platforms, Inc. and affiliates.

from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/embeddings")
async def read_example():
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