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

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment (skip this step if you didn't create a virtual environment):

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

5. Install dependencies:

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

# Good code quality

please run tests and pre-commit before submitting your PR.

# License

see the license file at the root directory: MIT
