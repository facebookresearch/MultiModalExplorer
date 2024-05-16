// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { Outlet } from "react-router-dom";

import ErrorAlert from "@components/ErrorAlert";
import { useAppContext } from "@providers/ContextProvider";

const PageLayout = () => {
  const { error, setError } = useAppContext();

  return (
    <main className="page-container h-screen w-screen">
      <ErrorAlert {...{ error, setError }} />
      <Outlet />
    </main>
  );
};

export default PageLayout;
