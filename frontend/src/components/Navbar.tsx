// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import Searchbar from "./Searchbar";

export default function Navbar(): JSX.Element {
  return (
    <nav className="navbar">
      <div className="fixed top-0 left-0 z-[1100] flex items-center justify-between w-full h-20 gap-6 px-4 bg-base-200">
        <h1 className="flex-none text-lg font-bold">
          Multimodal Embedding Visualizer
        </h1>
        <div className="flex justify-start w-full">
          <Searchbar />
        </div>
      </div>
    </nav>
  );
}
