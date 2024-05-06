/* eslint-disable react-hooks/exhaustive-deps */
// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useEffect, useRef, useCallback, useState, memo } from "react";
import { useSearchParams } from "react-router-dom";
import createScatterplot from "regl-scatterplot";
import * as d3 from "d3";
import Konva from "konva";
import { Layer as KonvaLayer } from "konva/lib/Layer";
import { useDebounce } from "react-use";

import { useAppContext } from "@providers/ContextProvider";
import { truncate } from "@utils";
import { POINT_COLOR_LIST } from "@constants";
import {
  EmbeddingsDetailsResponseProps,
  RenderEmbeddingsProps,
} from "types/embedding.types";
import { getEmbeddingPointDetails } from "@actions/api/embedding";

const MAX_ZOOM = 110;
const POINTS_ZOOM_START = 90;
const POINT_SIZE = 2;

const transitionProp = {
  transition: true,
  transitionDuration: 1000,
};

const RenderEmbeddings: React.FC<RenderEmbeddingsProps> = memo(
  ({ embeddings, handleEmdeddingSelect, handleEmdeddingUnselect }) => {
    // Get the handlers function from the app context
    const { setZoomHandlers } = useAppContext();

    const [width, setWidth] = useState<number>(1);
    const [height, setHeight] = useState<number>(1);
    const [points, setPoints] = useState<Array<number>>();

    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const stageRef = useRef<HTMLDivElement | null>(null);
    const layerRef = useRef<KonvaLayer | null>(null);
    const scatterplotRef = useRef(null);

    const [searchParams, setSearchParams] = useSearchParams();

    const {
      data: embeddingDetails,
      // isPending: loadingEmbeddingDetails,
      postData: fetchPointData,
    } = getEmbeddingPointDetails() as EmbeddingsDetailsResponseProps;

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
        pointData: Array<{ x: number; y: number; metadata: string; id: string }>
      ) => {
        const layer = layerRef.current;

        if (!layer || pointData.length <= 0) return;

        handleCleanData();

        pointData.forEach((item) => {
          const text = new Konva.Text({
            x: item.x,
            y: item.y,
            text: item.metadata,
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
        xScale: d3.ScaleLinear<number, number>,
        yScale: d3.ScaleLinear<number, number>
      ) => {
        const dataPoints = pointsInView.reduce((acc, point) => {
          const [x, y] = embeddings![point];
          const data = embeddingDetails?.find((item) => item.index === point);

          const metadata = data?.data;

          if (data) {
            acc.push({
              id: point.toString(),
              x: xScale(x),
              y: yScale(y),
              metadata: truncate(metadata, 100),
            });
          }
          return acc;
        }, [] as Array<{ id: string; x: number; y: number; metadata: string }>);

        handleDrawData(dataPoints);
      },
      [embeddings, handleDrawData, embeddingDetails]
    );

    // Handle the set query parameters
    const handleSetQueryParams = (scatterplot) => {
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
      }, 200);
    };

    // Handle the view event func from the scatterplot
    const handleView = useCallback(
      (xScale, yScale, scatterplot) => {
        const pointsInView = scatterplot.get("pointsInView");
        const getCamera = scatterplot.get("camera");

        getCamera.setScaleBounds([0, MAX_ZOOM]);

        const zoom = 1 / getCamera.distance[0];

        if (zoom > POINTS_ZOOM_START) {
          setPoints(pointsInView);
          handleShowData(pointsInView, xScale, yScale);
          // scatterplot.set({ opacity: [0] });
        } else {
          handleCleanData();
          // scatterplot.set({ opacity: [1] });
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

    // Create debounce timer func to fetch point data from API
    useDebounce(
      () => {
        if (points) fetchPointData({ points: points });
      },
      200,
      [points]
    );

    // Set up view event handler and subscribe to it
    useEffect(() => {
      const scatterplot = scatterplotRef.current!;
      if (!scatterplot) return;

      // @ts-expect-error "Type not supported by scatterplot"
      scatterplot.subscribe("view", ({ xScale, yScale }) => {
        handleSetQueryParams(scatterplot);
        handleView(xScale, yScale, scatterplot);
      });

      return () => {};
    }, [scatterplotRef.current, embeddingDetails]);

    // Initialize the scatterplot and set up event handlers
    useEffect(() => {
      const stageContainer = stageRef.current;

      if (!canvasRef.current || !stageContainer || !embeddings) return;

      const [xScale, yScale] = [
        d3.scaleLinear().domain([-1, 1]).range([0, width]),
        d3.scaleLinear().domain([-1, 1]).range([0, height]),
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

      scatterplot.draw(embeddings);

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
      <>
        <div className="absolute w-full h-[calc(100%-80px)] top-20 bottom-0">
          <canvas ref={canvasRef} className="w-full h-full" />
          <div
            ref={stageRef}
            className="absolute top-0 bottom-0 left-0 right-0 w-full h-full pointer-events-none"
          />
        </div>
      </>
    );
  }
);

export default RenderEmbeddings;
