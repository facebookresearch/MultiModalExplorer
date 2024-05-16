// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Loader from "./Loader";
import { EmbeddingDetailsProps } from "@type/embedding.types";

const EmbeddingDetails: React.FC<EmbeddingDetailsProps> = ({
  embeddingDetails,
  loadingEmbeddingDetails,
}) => {
  return (
    <aside className="fixed top-16 right-5 z-[999]">
      {!loadingEmbeddingDetails ? (
        <div className="card lg:w-[320px] max-w-[320px] bg-base-100 border-2 border-white rounded">
          {embeddingDetails && (
            <div className="flex flex-col justify-between min-h-56">
              <div className="border-b border-white card-body">
                <div className="flex items-center justify-center h-20 p-6 rounded">
                  <div className="font-bold">Data Preview</div>
                </div>
              </div>
              <div className="p-2 mt-0">
                <div className="flex flex-row items-center justify-between p-2 mb-2">
                  <div className="px-1 text-2xs lg:text-sm">
                    <h3 className="font-bold text-gray/50">Embedding ID</h3>
                    <h2 className="font-bold text-white">
                      {embeddingDetails?.id}
                    </h2>
                  </div>
                </div>
                <div className="p-3 bg-primary">
                  <p>Details description!</p>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center justify-center w-full h-56">
          <Loader />
        </div>
      )}
    </aside>
  );
};

export default EmbeddingDetails;
