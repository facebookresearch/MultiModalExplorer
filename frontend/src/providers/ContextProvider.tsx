// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-refresh/only-export-components */

import { createContext, ReactNode, useContext, useState } from "react";

interface AppContextType {
  store: any;
  setStore: React.Dispatch<React.SetStateAction<any>>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const initialData = {};

export const ContextProvider = ({ children }: { children: ReactNode }) => {
  const [store, setStore] = useState(initialData);

  const value: AppContextType = {
    store,
    setStore,
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
