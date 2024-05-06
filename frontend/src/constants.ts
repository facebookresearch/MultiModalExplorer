/* Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

import * as d3 from "d3";

export const API_BASE_URL = "http://127.0.0.1:8000/api";

const numClusters = 8;

const blueShades = d3
  .scaleSequential(d3.interpolateBlues)
  .domain([0, numClusters - 1]);

export const POINT_COLOR_LIST = Array.from({ length: numClusters }, (_, i) =>
  d3.rgb(blueShades(i)).formatHex()
);
