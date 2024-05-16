# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from multimodalexplorer.api.endpoints import create_router
from multimodalexplorer.utils.utils import parse_arguments

app = FastAPI()

args = parse_arguments()

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


app.include_router(create_router())

# Start the FastAPI server with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host=args["host"], port=int(args["port"]), reload=True)
