// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

interface EmbeddingsData {
  data: string;
  media_type: string;
  x: number;
  y: number;
  cluster: number;
  id: number;
  index: number;
}

type EmbeddingsPoint = [number, number, number];

export type EmbeddingsResponseProps = {
  data: Array<EmbeddingsPoint> | null;
  isPending: boolean;
};

export type EmbeddingsDetailsResponseProps = {
  data: Array<EmbeddingsData> | null;
  isPending: boolean;
  postData: (e) => void;
};

export type EmbeddingDetailsProps = {
  embeddingDetails: Array<EmbeddingsData> | null;
  loadingEmbeddingDetails: boolean;
};

export type RenderEmbeddingsProps = {
  embeddings: Array<EmbeddingsPoint> | null;
  handleEmdeddingSelect?: (detail: number[]) => Promise<void>;
  handleEmdeddingUnselect?: () => void;
};
