import { useEffect, useState } from "react";

import {
  RenderEmbeddings,
  Navbar,
  EmbeddingDetails,
  Footer,
  Loader,
} from "./components";
import { getEmbeddingPoints, getEmbeddingPointDetails } from "./actions";
import "./index.css";

function App() {
  const [embeddings, setEmbeddings] = useState<Array<[number, number, number]>>(
    []
  );

  const [embeddingPoint, setEmbeddingPoint] = useState<null | number[]>(null);

  const [embeddingDetails, setEmbeddingDetails] = useState<null | {
    id: number;
  }>(null);

  const [loadingEmbeddingDetails, setLoadingEmbeddingDetails] =
    useState<boolean>(false);

  useEffect(() => {
    const embeddings = async () => {
      const resp = await getEmbeddingPoints();
      setEmbeddings(resp);
    };
    embeddings();
  }, []);

  const handlePointClicked = async (point: number[]) => {
    setLoadingEmbeddingDetails(true);
    setEmbeddingPoint(point);

    const details = await getEmbeddingPointDetails(point);

    setEmbeddingDetails(details);
    setLoadingEmbeddingDetails(false);
  };

  const handlePointUnclicked = () => {
    setEmbeddingDetails(null);
    setEmbeddingPoint(null);
    setLoadingEmbeddingDetails(false);
  };

  return (
    <div className="visualizer-page">
      <Navbar />
      {embeddings?.length ? (
        <>
          <RenderEmbeddings
            embeddings={embeddings}
            handlePointClicked={handlePointClicked}
            handlePointUnclicked={handlePointUnclicked}
          />

          <EmbeddingDetails
            embeddingPoint={embeddingPoint}
            embeddingDetails={embeddingDetails}
            loadingEmbeddingDetails={loadingEmbeddingDetails}
          />
          <Footer />
        </>
      ) : (
        <div className="w-screen h-screen flex justify-center items-center">
          <Loader />
        </div>
      )}
    </div>
  );
}

export default App;
