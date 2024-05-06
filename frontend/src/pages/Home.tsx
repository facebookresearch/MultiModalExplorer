// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Loader from "@components/Loader";
import RenderEmbeddings from "@components/RenderEmbeddings";

import { getEmbeddingPoints } from "@actions/api/embedding";
import { EmbeddingsResponseProps } from "@type/embedding.types";

export default function Home(): JSX.Element {
  const { data: embeddings, isPending } =
    getEmbeddingPoints() as EmbeddingsResponseProps;

  const handleEmdeddingSelect = async () => {};

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
        </>
      ) : (
        <div className="flex items-center justify-center w-screen h-screen">
          <Loader />
        </div>
      )}
    </div>
  );
}
