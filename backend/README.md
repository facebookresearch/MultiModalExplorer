The backend is found here.

It is written with FastAPI.

Install with poetry.
Add dependencies with `poetry add`

You can run it with:
`poetry run uvicorn main:app`

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/facebookresearch/MultiModalExplorer.git`
   ```

2. Navigate to the project directory:

   ```bash
   cd MultiModalExplorer/backend/multimodalexplorer`
   ```

3. Install dependencies:

   ```bash
   poetry install
   ```

## Usage

1. To run process-datasets script:

   ```bash
   python -m functions.process_datasets
   ```

2. To run reduce_embed_dims script:

   ```bash
   python -m functions.reduce_embed_dims
   ```

3. To run create_faiss_index script:

   ```bash
   python -m functions.create_faiss_index
   ```

4. Run the following command to start the uvicorn server:
   ```bash
   python main.py
   ```

## Project Configuration

The [config.json](./multimodalexplorer/config.json) outlines the configuration settings used within the project.

- Datasets
  - Type: Specifies the type of dataset.
  - Name: Specifies the path to the dataset directory.
  - Source Language: Specifies the source language of the dataset.
- File Paths
  - raw_data_file: Path to the directory containing raw data files.
  - embed_file: Path to the directory containing embedding files.
  - umap_file: Path to the directory containing UMAP files.
  - index_file: Path to the directory containing index files.
- Parameters
  - batch_size: Batch size used during data processing.
  - chunk_size: Chunk size used during data processing.
  - train_data_size: Size of the training dataset.
  - dataset_sample_size: Size of the dataset sample used.
- Index Arguments
  - k_neighbors: Number of neighbors used in the index.
- UMAP Arguments
  - n_components: Number of dimensions in the UMAP embedding.
  - n_neighbors: Number of neighbors used in UMAP.
  - min_dist: Minimum distance used in UMAP.
  - metric: Distance metric used in UMAP.
- Cluster Arguments
  - min_samples: Minimum number of samples in a cluster.
  - min_cluster_size: Minimum size of a cluster.
- Host and Port
  - host: Host address for the server.
  - port: Port number for the server.

# Good code quality

please run tests and pre-commit before submitting your PR.

# License

see the license file at the root directory: MIT
