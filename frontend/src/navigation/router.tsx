/**
 * (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.
 */

import { createBrowserRouter } from "react-router-dom";

import Home from "../pages/Home";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
]);
