// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { RouterProvider } from "react-router-dom";

import { router } from "@navigation/router";
import Navbar from "@components/Navbar";
import Footer from "@components/Footer";
import { ContextProvider } from "@providers/ContextProvider";

import "./index.css";

function App() {
  return (
    <div className="visualizer">
      <ContextProvider>
        <Navbar />
        <RouterProvider router={router} />
        <Footer />
      </ContextProvider>
    </div>
  );
}

export default App;
