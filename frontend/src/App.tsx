/**
 * (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.
 */

import { RouterProvider } from "react-router-dom";
import { router } from "./navigation/router";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./index.css";

function App() {
  return (
    <div className="visualizer-page">
      <Navbar />
      <RouterProvider router={router} />
      <Footer />
    </div>
  );
}

export default App;
