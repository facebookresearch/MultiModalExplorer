# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import os

import torch


def get_file_path(file_name, dir_name="../db"):
    folder_path = os.path.join(os.path.dirname(__file__), dir_name)
    os.makedirs(folder_path, exist_ok=True)
    return os.path.join(folder_path, file_name)


def index_to_gpu(index, faiss):
    co = faiss.GpuMultipleClonerOptions()
    co.useFloat16 = True
    index = faiss.index_cpu_to_all_gpus(index, co=co)
    return index


def load_embeddings_from_files(dirname):
    embeddings_list = []

    folder_name = f"../{dirname}"
    folder_path = os.path.join(os.path.dirname(__file__), folder_name)

    files = os.listdir(folder_path)

    # Sort files according to their order in the folder
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            embeddings = torch.load(file_path)
            embeddings_list.append(embeddings)

    return torch.cat(embeddings_list, dim=0)
