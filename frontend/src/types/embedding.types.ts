// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

interface Embeddings {
  data: string;
  media_type: string;
  x: number;
  y: number;
  cluster: number;
  id: number;
}

export type EmbeddingsResponseProps = {
  data: Array<Embeddings> | null;
  isPending: boolean;
};

export type EmbeddingsDetailsResponseProps = {
  data: Embeddings | null;
  isPending: boolean;
  sendData: (e) => void;
};

export type RenderEmbeddingsProps = {
  embeddings: Array<Embeddings> | null;
  handleEmdeddingSelect?: (detail: number[]) => Promise<void>;
  handleEmdeddingUnselect?: () => void;
};
export type EmbeddingDetailsProps = {
  embeddingDetails: Embeddings | null;
  loadingEmbeddingDetails: boolean;
};
