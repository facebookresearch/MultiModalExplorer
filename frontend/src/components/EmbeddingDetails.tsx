// Copyright (c) Meta Platforms, Inc. and affiliates
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

/**
 * (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.
 */

import Loader from "./Loader";
interface EmbeddingDetailsProps {
  embeddingPoint?: number[] | null;
  embeddingDetails?: { id: number } | null;
  loadingEmbeddingDetails: boolean;
}

const EmbeddingDetails: React.FC<EmbeddingDetailsProps> = ({
  embeddingPoint,
  embeddingDetails,
  loadingEmbeddingDetails,
}) => {
  return (
    <aside className="fixed top-16 right-5 z-[999]">
      {embeddingPoint && (
        <div className="card lg:w-[320px] max-w-[320px] bg-base-100 border-2 border-white rounded">
          {!loadingEmbeddingDetails && embeddingDetails ? (
            <div className="flex flex-col justify-between min-h-56">
              <div className="card-body border-b border-white">
                <div className="h-20 p-6 rounded flex justify-center items-center">
                  <div className="font-bold">Data Preview</div>
                </div>
              </div>
              <div className="p-2 mt-0">
                <div className="flex flex-row justify-between items-center mb-2 p-2">
                  <div className="px-1 text-2xs lg:text-sm">
                    <h3 className="font-bold text-gray/50">Embedding ID</h3>
                    <h2 className="text-white font-bold">
                      {embeddingDetails?.id}
                    </h2>
                  </div>
                </div>
                <div className="p-3 bg-primary">
                  <p>Details description!</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="w-full h-56 flex justify-center items-center">
              <Loader />
            </div>
          )}
        </div>
      )}
    </aside>
  );
};

export default EmbeddingDetails;
