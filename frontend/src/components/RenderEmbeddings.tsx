// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

/* eslint-disable react-hooks/exhaustive-deps */

import React, { useEffect, useRef, useCallback } from "react";
import createScatterplot from "regl-scatterplot";
import { scaleLinear } from "d3-scale";

interface RenderEmbeddingsProps {
  pointSize?: number;
  embeddings: Array<[number, number, number]>;
  handleEmdeddingSelect?: (detail: number[]) => Promise<void>;
  handleEmdeddingUnselect?: () => void;
}

const maxPointLabels = 50;
const pointColor = [
  "#d192b7",
  "#6fb2e4",
  "#eecb62",
  "#56bf92",
  "#dca237",
  "#3a84cc",
  "#c76526",
  "#9c11d8",
  "#71ff82",
];

const RenderEmbeddings: React.FC<RenderEmbeddingsProps> = ({
  pointSize = 1,
  embeddings,
  handleEmdeddingSelect,
  handleEmdeddingUnselect,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const textOverlayRef = useRef<HTMLCanvasElement>(null);

  const handleSelect = useCallback(({ points }: { points: number[] }) => {
    if (handleEmdeddingSelect) handleEmdeddingSelect(points);
  }, []);

  const handleDeselect = () => {
    if (handleEmdeddingUnselect) handleEmdeddingUnselect();
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const textOverlayEl = textOverlayRef.current;

    if (!canvas || !textOverlayEl || embeddings.length === 0) return;

    const { width, height } = canvas.getBoundingClientRect();

    const xScale = scaleLinear().domain([-1, 1]).range([0, width]);
    const yScale = scaleLinear().domain([-1, 1]).range([height, 0]);

    const scatterplot = createScatterplot({
      canvas: canvas,
      pointSize,
      width,
      height: height,
      xScale,
      yScale,
      showReticle: true,
    });

    scatterplot.draw(embeddings);

    scatterplot.set({
      deselectOnDblClick: true,
      colorBy: "category",
      pointColor,
    });

    scatterplot.subscribe("select", handleSelect);

    scatterplot.subscribe("deselect", handleDeselect);

    const resizeTextOverlay = () => {
      const { width, height } = canvas!.parentElement!.getBoundingClientRect();

      textOverlayEl.width = width * window.devicePixelRatio;
      textOverlayEl.height = height * window.devicePixelRatio;
      textOverlayEl.style.width = `${width}px`;
      textOverlayEl.style.height = `${height}px`;
    };

    resizeTextOverlay();
    window.addEventListener("resize", resizeTextOverlay);

    const overlayFontSize = 12;
    const textOverlayCtx = textOverlayEl.getContext("2d");

    if (!textOverlayCtx) return;

    textOverlayCtx.font = `${
      overlayFontSize * window.devicePixelRatio
    }px sans-serif`;
    textOverlayCtx.textAlign = "center";

    const handleView = () => {
      const showPointLabels = (pointsInView: number[]) => {
        clearPointLabels();
        textOverlayCtx.fillStyle = "rgb(255, 255, 255)";

        for (let i = 0; i < pointsInView.length; i++) {
          const [x, y] = embeddings[pointsInView[i]];
          const xPixel = xScale(x) * window.devicePixelRatio;
          const yPixel =
            yScale(y) * window.devicePixelRatio -
            overlayFontSize * 1.2 * window.devicePixelRatio;

          textOverlayCtx.fillText(pointsInView[i].toString(), xPixel, yPixel);
        }
      };

      const clearPointLabels = () => {
        textOverlayCtx.clearRect(
          0,
          0,
          width * window.devicePixelRatio,
          height * window.devicePixelRatio
        );
      };

      const pointsInView = scatterplot.get("pointsInView");

      if (pointsInView.length <= maxPointLabels) {
        showPointLabels(pointsInView);
      } else {
        clearPointLabels();
      }
    };

    scatterplot.subscribe("view", handleView);

    return () => {
      scatterplot.destroy();
      window.removeEventListener("resize", resizeTextOverlay);
    };
  }, [embeddings]);

  return (
    <div className="w-screen h-screen pb-4">
      <canvas ref={canvasRef} className="!w-full !h-full" />
      <canvas
        ref={textOverlayRef}
        className="!w-full !h-full absolute top-0 right-0 pointer-events-none"
      />
    </div>
  );
};

export default RenderEmbeddings;
