// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Loader from "@components/Loader";
import RenderEmbeddings from "@components/RenderEmbeddings";
import EmbeddingDetails from "@components/EmbeddingDetails";

import {
  getEmbeddingPointDetails,
  getEmbeddingPoints,
} from "@actions/api/embedding";
import {
  EmbeddingsDetailsResponseProps,
  EmbeddingsResponseProps,
} from "@type/embedding.types";

export default function Home(): JSX.Element {
  const { data: embeddings, isPending } =
    getEmbeddingPoints() as EmbeddingsResponseProps;

  const {
    data: embeddingDetails,
    isPending: loadingEmbeddingDetails,
    sendData,
  } = getEmbeddingPointDetails() as EmbeddingsDetailsResponseProps;

  const handleEmdeddingSelect = async (point: number[]) => {
    await sendData(point);
  };

  const handleEmdeddingUnselect = () => {};

  return (
    <div className="home-page">
      {!isPending ? (
        <>
          <RenderEmbeddings
            embeddings={embeddings}
            handleEmdeddingSelect={handleEmdeddingSelect}
            handleEmdeddingUnselect={handleEmdeddingUnselect}
          />

          <EmbeddingDetails
            embeddingDetails={embeddingDetails}
            loadingEmbeddingDetails={loadingEmbeddingDetails}
          />
        </>
      ) : (
        <div className="flex items-center justify-center w-screen h-screen">
          <Loader />
        </div>
      )}
    </div>
  );
}
