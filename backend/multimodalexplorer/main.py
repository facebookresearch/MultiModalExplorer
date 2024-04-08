# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from multimodalexplorer.api.endpoints import create_router

from .functions.create_faiss_index import process_data

app = FastAPI()

# Configure CORS
allowed_origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to MultiModalExplorer."}


def main():
    process_data()


if __name__ == "__main__":
    main()
    print("FAISS index created")

app.include_router(create_router())
