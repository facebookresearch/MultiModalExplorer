import { useEffect, useState } from "react";

import { Scatterplot, Navbar } from "./components";

import { getEmbeddingPoints } from "./actions";

import "./index.css";

function App() {
  const [embeddings, setEmbeddings] = useState<[number, number][]>([]);

  useEffect(() => {
    const embeddings = async () => {
      const resp = await getEmbeddingPoints();
      setEmbeddings(resp);
    };
    embeddings();
  }, []);

  return (
    <div className="plot-page">
      <Navbar />
      <Scatterplot embeddings={embeddings} />
    </div>
  );
}

export default App;
