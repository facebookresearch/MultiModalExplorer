# Copyright (c) Meta Platforms, Inc. and affiliates.

from datasets import load_dataset

def load_datasets():
    loaded_dataset = load_dataset("embedding-data/sentence-compression")

    trained_dataset = loaded_dataset["train"]

    dataset = [entry["set"][0] for entry in trained_dataset]

    return dataset

def process_data():
    load_datasets()