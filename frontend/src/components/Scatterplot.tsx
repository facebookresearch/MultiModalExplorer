import { useEffect, useRef } from "react";
import createScatterplot from "regl-scatterplot";

import { Loader } from ".";

interface ScatterplotViewProps {
  pointSize?: number;
  embeddings: [number, number][];
}

const Scatterplot: React.FC<ScatterplotViewProps> = ({
  pointSize = 4,
  embeddings,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const { width, height } = canvasRef.current.getBoundingClientRect();

    const scatterplot = createScatterplot({
      canvas: canvasRef.current,
      pointSize,
      width,
      height: height - 60,
      lassoOnLongPress: true,
    });

    scatterplot.subscribe("select", ({ points }) => {
      console.log(points, canvasRef.current);
      canvasRef.current!.dispatchEvent(new Event("input"));
    });

    scatterplot.draw(embeddings);

    return () => {
      scatterplot.destroy();
    };
  }, [pointSize, embeddings]);

  return (
    <>
      {embeddings.length ? (
        <canvas ref={canvasRef} className="w-full h-full" />
      ) : (
        <Loader />
      )}
    </>
  );
};

export default Scatterplot;
