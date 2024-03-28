// Copyright (c) Meta Platforms, Inc. and affiliates
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.

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
