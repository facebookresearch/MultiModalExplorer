# Copyright (c) Meta Platforms, Inc. and affiliates.

from fastapi import APIRouter

from . import embeddings, search


def create_router():
    router = APIRouter()

    router.include_router(
        embeddings.router, prefix="/api/embedding", tags=["embedding"]
    )
    router.include_router(search.router, prefix="/api/search", tags=["search"])

    return router
