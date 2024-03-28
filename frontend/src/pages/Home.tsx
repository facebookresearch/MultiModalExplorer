// Copyright (c) Meta Platforms, Inc. and affiliates
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

/**
 * (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.
 */

import { useEffect, useState } from "react";

import Loader from "../components/Loader";
import RenderEmbeddings from "../components/RenderEmbeddings";
import EmbeddingDetails from "../components/EmbeddingDetails";

import {
  getEmbeddingPointDetails,
  getEmbeddingPoints,
} from "../actions/api/embedding";

export default function Home() {
  // state for storing embeddings
  const [embeddings, setEmbeddings] = useState<Array<[number, number, number]>>(
    []
  );

  // state for storing a single embedding point
  const [embeddingPoint, setEmbeddingPoint] = useState<null | number[]>(null);

  // state for storing details of a single embedding
  const [embeddingDetails, setEmbeddingDetails] = useState<null | {
    id: number;
  }>(null);

  // state for indicating whether embedding details are being loaded
  const [loadingEmbeddingDetails, setLoadingEmbeddingDetails] =
    useState<boolean>(false);

  useEffect(() => {
    const fetchEmbeddings = async () => {
      const resp = await getEmbeddingPoints();
      setEmbeddings(resp);
    };
    fetchEmbeddings();
  }, []);

  const handleEmdeddingSelect = async (point: number[]) => {
    setLoadingEmbeddingDetails(true);
    setEmbeddingPoint(point);

    const details = await getEmbeddingPointDetails(point);

    setEmbeddingDetails(details);
    setLoadingEmbeddingDetails(false);
  };

  const handleEmdeddingUnselect = () => {
    setEmbeddingDetails(null);
    setEmbeddingPoint(null);
    setLoadingEmbeddingDetails(false);
  };

  return (
    <div className="home-page">
      {embeddings?.length ? (
        <>
          <RenderEmbeddings
            embeddings={embeddings}
            handleEmdeddingSelect={handleEmdeddingSelect}
            handleEmdeddingUnselect={handleEmdeddingUnselect}
          />

          <EmbeddingDetails
            embeddingPoint={embeddingPoint}
            embeddingDetails={embeddingDetails}
            loadingEmbeddingDetails={loadingEmbeddingDetails}
          />
        </>
      ) : (
        <div className="w-screen h-screen flex justify-center items-center">
          <Loader />
        </div>
      )}
    </div>
  );
}
