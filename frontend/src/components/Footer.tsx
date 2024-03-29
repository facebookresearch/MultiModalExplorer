// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

export default function Footer() {
  return (
    <div className="absolute bottom-2 left-2 flex flex-row z-[998]">
      <div className="hidden lg:flex bg-black/80">
        <div className="text-sm p-3">
          <p>Drag to pan</p>
          <p>Scroll to zoom in/out</p>
          <p>Click to select an embedding</p>
          <p>Double-click to deselect an embedding</p>
        </div>
      </div>
    </div>
  );
}
