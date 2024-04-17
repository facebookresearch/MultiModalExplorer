# MultiModalExplorer, a tool to explore embedding spaces

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Development Environment Setup

To set up the development environment for MultiModalExplorer, follow these steps:

1. Clone the repository

```bash
git clone https://github.com/facebookresearch/MultiModalExplorer.git
```

2. Navigate to the project directory

```bash
cd MultiModalExplorer
```

3. Run docker-compose to build the development environment

```bash
docker compose up --build
```

This command will build and start the backend and frontend servers. The frontend server will be available at `http://localhost:5173`.

# Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for how to help out.

# License
MultiModalExplorer is MIT licensed, as found in the LICENSE file.
