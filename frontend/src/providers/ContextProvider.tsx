// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-refresh/only-export-components */

import { createContext, ReactNode, useContext, useState } from "react";

interface AppContextType {
  error: any;
  setError: (e: any) => void;
  zoomHandlers: any;
  setZoomHandlers: (e: any) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const ContextProvider = ({ children }: { children: ReactNode }) => {
  const [error, setError] = useState({
    isError: false,
    errorMsg: null,
  });

  const [zoomHandlers, setZoomHandlers] = useState();

  const value: AppContextType = {
    error,
    setError,
    zoomHandlers,
    setZoomHandlers,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => {
  const context = useContext(AppContext);

  if (!context) {
    throw new Error("useAppContext must be used within a ContextProvider");
  }

  return context;
};
