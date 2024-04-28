/* eslint-disable react-hooks/exhaustive-deps */
// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useEffect, useRef, useCallback, useState, memo } from "react";
import createScatterplot from "regl-scatterplot";
import { scaleLinear } from "d3-scale";
import Konva from "konva";
import { Layer as KonvaLayer } from "konva/lib/Layer";

import { useAppContext } from "@providers/ContextProvider";
import { truncate } from "@utils";
import { useSearchParams } from "react-router-dom";
import { POINT_COLOR_LIST } from "@constants";
import { RenderEmbeddingsProps } from "types/embedding.types";

const MAX_POINT_LABEL = 15;
const POINT_SIZE = 3;

const transitionProp = {
  transition: true,
  transitionDuration: 1000,
};

const RenderEmbeddings: React.FC<RenderEmbeddingsProps> = memo(
  ({ embeddings, handleEmdeddingSelect, handleEmdeddingUnselect }) => {
    // Get the handlers function from the app context
    const { setZoomHandlers } = useAppContext();

    const [width, setWidth] = useState(1);
    const [height, setHeight] = useState(1);

    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const stageRef = useRef<HTMLDivElement | null>(null);
    const layerRef = useRef<KonvaLayer | null>(null);
    const scatterplotRef = useRef(null);

    const [searchParams, setSearchParams] = useSearchParams();

    // Handle embedding selection
    const handleSelect = useCallback(
      ({ points }: { points: number[] }) => {
        handleEmdeddingSelect?.(points);
      },
      [handleEmdeddingSelect]
    );

    // Handle embedding deselection
    const handleDeselect = useCallback(() => {
      handleEmdeddingUnselect?.();
    }, [handleEmdeddingUnselect]);

    // Zoom to a specific point in the scatterplot
    const handleZoomToPoint = useCallback(
      (id: number) => {
        // @ts-expect-error "Type not supported by scatterplot"
        scatterplotRef.current?.zoomToPoints([id], {
          padding: 0.2,
          ...transitionProp,
        });
      },
      [scatterplotRef]
    );

    // Zoom to the origin of the scatterplot
    const handleZoomToOrigin = useCallback(() => {
      // @ts-expect-error "Type not supported by scatterplot"
      scatterplotRef?.current?.zoomToOrigin({
        ...transitionProp,
      });
    }, [scatterplotRef]);

    // Zoom to a specific area in the scatterplot
    const handleZoomToArea = useCallback(() => {
      // @ts-expect-error "Type not supported by scatterplot"
      scatterplotRef.current?.zoomToArea(
        { x: 0, y: 0, width: 0.03, height: 0.03 },
        { ...transitionProp }
      );
    }, [scatterplotRef]);

    // Clean the data layer
    const handleCleanData = useCallback(() => {
      layerRef.current?.destroyChildren();
    }, []);

    // Draw data points on the canvas
    const handleDrawData = useCallback(
      (
        pointData: Array<{ x: number; y: number; data: string; id: string }>
      ) => {
        const layer = layerRef.current;

        if (!layer || pointData.length <= 0) return;

        handleCleanData();

        pointData.forEach((item) => {
          const text = new Konva.Text({
            x: item.x,
            y: item.y,
            text: item.data,
            fontSize: 14,
            fill: "white",
            width: 250,
            padding: 8,
            wrap: "word",
            lineHeight: 1.2,
          });

          const rect = new Konva.Rect({
            x: item.x,
            y: item.y,
            stroke: "#555",
            strokeWidth: 1,
            fill: "#121212",
            width: text.width(),
            height: text.height(),
            cornerRadius: 5,
          });

          layer.add(rect);
          layer.add(text);
        });

        layer.batchDraw();
      },
      [handleCleanData]
    );

    // Show data points based on the points in view
    const handleShowData = useCallback(
      (
        pointsInView: number[],
        xScale: scaleLinear<number, number>,
        yScale: scaleLinear<number, number>
      ) => {
        const dataPoints = pointsInView.reduce((acc, point) => {
          const { x, y, data } = embeddings![point];
          acc.push({
            id: point.toString(),
            point,
            x: xScale(x),
            y: yScale(y),
            data: truncate(data, 100),
          });
          return acc;
        }, [] as Array<{ id: string; point: number; x: number; y: number; data: string }>);

        handleDrawData(dataPoints);
      },
      [embeddings, handleDrawData]
    );

    // Handle the view event from the scatterplot
    const handleView = useCallback(
      (xScale, yScale) => {
        const scatterplot = scatterplotRef.current!;

        if (!scatterplot) return;

        // @ts-expect-error "Type not supported by scatterplot"
        const getCamera = scatterplot.get("camera");

        let timer = undefined as ReturnType<typeof setTimeout> | undefined;

        if (timer) {
          clearTimeout(timer);
        }

        timer = setTimeout(() => {
          const setQueryParameters = new URLSearchParams();
          setQueryParameters.set(
            "at",
            `${getCamera.target[0]},${getCamera.target[1]},${getCamera.distance[0]}`
          );
          setSearchParams(setQueryParameters, { replace: true });
        }, 1000);

        // @ts-expect-error "Type not supported by scatterplot"
        const pointsInView = scatterplot.get("pointsInView");

        if (pointsInView.length <= MAX_POINT_LABEL) {
          handleShowData(pointsInView, xScale, yScale);
          // @ts-expect-error "Type not supported by scatterplot"
          scatterplot.set({ opacity: [0] });
        } else {
          handleCleanData();
          // @ts-expect-error "Type not supported by scatterplot"
          scatterplot.set({ opacity: [1] });
        }
      },
      [handleCleanData, handleShowData]
    );

    // Set the width and height of the canvas based on the parent element
    useEffect(() => {
      const canvas = canvasRef.current;
      const wrapper = canvas?.parentElement?.getBoundingClientRect();
      setWidth(wrapper!.width);
      setHeight(wrapper!.height);
    }, [canvasRef.current]);

    // Initialize the scatterplot and set up event handlers
    useEffect(() => {
      const stageContainer = stageRef.current;

      if (!canvasRef.current || !stageContainer || embeddings?.length === 0)
        return;

      const [xScale, yScale] = [
        scaleLinear().domain([-1, 1]).range([0, width]),
        scaleLinear().domain([-1, 1]).range([0, height]),
      ];

      const camara_pos = searchParams.get("at");

      const scatterplot = createScatterplot({
        canvas: canvasRef.current,
        pointSize: POINT_SIZE,
        width,
        height,
        xScale,
        yScale,
      });

      const stage = new Konva.Stage({
        container: stageContainer,
        width,
        height,
      });

      const layer = new Konva.Layer();
      layerRef.current = layer;

      stage.add(layer);

      scatterplot.draw(
        embeddings?.length
          ? embeddings?.map((embed) => [embed.x, embed.y, embed.cluster])
          : []
      );

      scatterplot.set({
        deselectOnDblClick: true,
        colorBy: "category",
        pointColor: POINT_COLOR_LIST,
        showReticle: true,
        cameraTarget: camara_pos
          ? [
              parseFloat(camara_pos.split(",")[0]),
              parseFloat(camara_pos.split(",")[1]),
            ]
          : [0, 0],
        cameraDistance: camara_pos ? parseFloat(camara_pos.split(",")[2]) : 1,
      });

      scatterplot.subscribe("select", handleSelect);
      scatterplot.subscribe("deselect", handleDeselect);

      scatterplot.subscribe("view", ({ xScale, yScale }) =>
        handleView(xScale, yScale)
      );

      // @ts-expect-error "Type not supported by scatterplot"
      scatterplotRef.current = scatterplot;

      return () => {
        scatterplot.destroy();
      };
    }, [width, height, embeddings]);

    useEffect(() => {
      if (scatterplotRef.current) {
        setZoomHandlers({
          handleZoomToPoint,
          handleZoomToOrigin,
          handleZoomToArea,
        });
      }
    }, [scatterplotRef.current]);

    return (
      <div className="absolute w-full h-[calc(100%-80px)] top-20 bottom-0">
        <canvas ref={canvasRef} className="w-full h-full" />
        <div
          ref={stageRef}
          className="absolute top-0 bottom-0 left-0 right-0 w-full h-full pointer-events-none"
        />
      </div>
    );
  }
);

export default RenderEmbeddings;
