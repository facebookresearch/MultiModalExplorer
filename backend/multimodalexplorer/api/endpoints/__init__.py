# Copyright (c) Meta Platforms, Inc. and affiliates.

from fastapi import APIRouter

from . import embeddings


def create_router():
    router = APIRouter()
    router.include_router(embeddings.router, prefix="/api", tags=["embeddings"])
    return router
