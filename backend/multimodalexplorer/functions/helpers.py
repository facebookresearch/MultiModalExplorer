# Copyright (c) Meta Platforms, Inc. and affiliates.

import os

import pandas as pd


def save_data_as_file(data, file_name, folder="../db"):
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    os.makedirs(folder_path, exist_ok=True)
    csv_path = os.path.join(folder_path, f"{file_name}.tsv")

    df = pd.DataFrame(data)

    df.to_csv(csv_path, sep="\t", index=False)


def index_to_gpu(index, faiss):
    co = faiss.GpuMultipleClonerOptions()
    co.useFloat16 = True
    index = faiss.index_cpu_to_all_gpus(index, co=co)
    return index
