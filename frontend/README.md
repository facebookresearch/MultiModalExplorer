# MultiModalExplorer, a tool to explore embedding spaces

This is a project aimed at creating a multimodal embedding visualizer using React, TypeScript, and Vite. It provides a user interface to visualize embeddings generated from multiple modalities such as text, images, videos and audio.

## Features

- Visualize embeddings from different modalities.
- Interactively explore similarities and relationships between embeddings.
- Easy-to-use interface for comparing and analyzing multimodal embeddings.

## Technologies Used

- React
- TypeScript
- Vite
- TailwindCSS

## Getting Started

To run the frontend of the MultiModalExplorer, follow these steps:

## Prerequisites

- Make sure you have Node.js and pnpm installed on your system.
- Backend server running. Follow the instructions [here](/backend/README.md) to set it up.

## Installation

1. Clone this repository to your local machine:

   `git clone https://github.com/facebookresearch/MultiModalExplorer.git`

2. Navigate to the project directory:

   `cd MultiModalExplorer/frontend`

3. Install dependencies:

   `pnpm install or pnpm i`

## Running the Frontend

Start the development server:

`pnpm dev`

This will start the frontend server at `http://localhost:5173/`

## Running the Backend

Before you can fully utilize the visualizer, you need to ensure the backend server is running. Please follow the instructions provided in the backend repository [here](/backend/README.md).

## Building for Production

To build the frontend for production, run:

`pnpm build`

This will create a production-ready build of the frontend in the `build` directory.

## Contributing

See the [CONTRIBUTING](/CONTRIBUTING.md) file for how to help out.

## License

MultiModalExplorer is MIT licensed, as found in the [LICENSE](/LICENSE) file.
