# Copyright (c) Meta Platforms, Inc. and affiliates.

import torch
from datasets import load_dataset
from imagebind import data as imagebind_data
from imagebind.models import imagebind_model

from .helpers import save_data_as_file

# Determine the device (CPU or GPU) for torch operations
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Instantiate imagebind model
model = imagebind_model.imagebind_huge(pretrained=True)
model.eval()
model.to(DEVICE)

# Dictionary storing data loader functions based on modality
MODALITY_KEYS = {
    "text": {
        "data_loader_function": imagebind_data.load_and_transform_text
    },
    "image": {
        "data_loader_function": imagebind_data.load_and_transform_vision_data
    }
}

def load_datasets():
    # Load dataset from huggingface dataset
    loaded_dataset = load_dataset("embedding-data/sentence-compression")

    # Select the training subset of the loaded dataset
    trained_dataset = loaded_dataset["train"]

    # Extract the sentences from each entry in the training dataset
    dataset = [entry["set"][0] for entry in trained_dataset]

    return dataset

def generate_embedding():
    # Load text dataset
    text_dataset = load_datasets()

    # Dictionary containing all datasets
    all_datasets = {
        'text': text_dataset,
    }

    # Dictionary to hold input data for the model
    dataset_input = {}

    # Load data for each modality using corresponding data loader function
    for key, val in all_datasets.items():
        dataset_input[key] = MODALITY_KEYS[key]['data_loader_function'](val, DEVICE)

    # Compute embeddings for each modality
    with torch.no_grad():
        embeddings = model(dataset_input)

    # Concatenate tensors for different modalities
    concatenated_tensors = []

    for _, tensor in embeddings.items():
        concatenated_tensors.append(tensor)

    combined_tensor = torch.cat(concatenated_tensors, dim=0)

    # Save combined tensor embedding as a file
    save_data_as_file(combined_tensor, 'combined_tensor_embedding')

    return [combined_tensor, all_datasets]

def process_data():
    [embeddings, all_datasets] = generate_embedding()
