# Copyright (c) Meta Platforms, Inc. and affiliates.

from fastapi import APIRouter

from .embeddings import create_embeddings_router
from .search import create_search_router


def create_router(args):
    router = APIRouter()

    router.include_router(
        create_embeddings_router(), prefix="/api/embedding", tags=["embedding"]
    )
    router.include_router(
        create_search_router(args), prefix="/api/search", tags=["search"]
    )
    return router
