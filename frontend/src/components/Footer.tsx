// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { RiZoomInFill, RiZoomOutFill } from "react-icons/ri";

import metaAILogo from "@assets/icons/metaAI-white-logo.svg";
import { useAppContext } from "@providers/ContextProvider";

interface ZoomButton {
  name: string;
  Icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  action: string;
}

export default function Footer(): JSX.Element {
  const { zoomHandlers } = useAppContext();

  // Define the zoomBtns array with type annotation
  const zoomBtns: ZoomButton[] = [
    { name: "zoomplus", Icon: RiZoomInFill, action: "handleZoomToArea" },
    {
      name: "zoomminus",
      Icon: RiZoomOutFill,
      action: "handleZoomToOrigin",
    },
  ];

  return (
    <footer className="footer">
      <div className="fixed bottom-0 left-0 flex z-[1000] justify-between items-end w-full">
        <div className="flex items-center p-3 bg-black/80">
          {zoomBtns.map((item) => (
            <div
              className="flex items-center px-2 border-r-2 cursor-pointer"
              key={item.name}
            >
              <item.Icon
                className="w-8 h-8 cursor-pointer"
                onClick={zoomHandlers?.[item.action]}
              />
            </div>
          ))}
          <div className="px-3 text-xs">
            <p>Drag to pan</p>
            <p>Scroll to zoom in/out</p>
            <p>Click to select an embedding</p>
            <p>Double-click to deselect an embedding</p>
          </div>
        </div>
        <div className="m-8">
          <img className="w-20 h-3" src={metaAILogo} alt=""></img>
        </div>
      </div>
    </footer>
  );
}
