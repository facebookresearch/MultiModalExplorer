// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { createBrowserRouter } from "react-router-dom";

import Home from "@pages/Home";
import PageLayout from "layouts/PageLayout";

export const router = createBrowserRouter([
  {
    path: "/",
    children: [
      {
        element: <PageLayout />,
        children: [{ index: true, element: <Home /> }],
      },
    ],
  },
]);
