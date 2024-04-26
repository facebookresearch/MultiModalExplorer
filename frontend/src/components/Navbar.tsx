// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Searchbar from "./Searchbar";

export default function Navbar(): JSX.Element {
  return (
    <nav className="navbar">
      <div className="fixed top-0 left-0 px-4 z-50 bg-base-200 flex justify-between items-center h-20 gap-6 w-full">
        <h1 className="text-lg font-bold flex-none">
          Multimodal Embedding Visualizer
        </h1>
        <div className="flex w-full justify-start">
          <Searchbar />
        </div>
      </div>
    </nav>
  );
}
