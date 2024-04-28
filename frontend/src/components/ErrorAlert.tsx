// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { useCallback, useEffect } from "react";
import { MdErrorOutline } from "react-icons/md";

import { clx } from "@utils";

interface ErrorAlertProps {
  error: { isError: boolean; errorMsg: string | null };
  setError: (e) => void;
  delay?: number;
}

const ErrorAlert = ({ error, setError, delay = 5000 }: ErrorAlertProps) => {
  const handleClose = useCallback(() => {
    setError({
      isError: false,
      errorMsg: null,
    });
  }, [setError]);

  useEffect(() => {
    if (error?.isError) {
      const timer = setTimeout(() => handleClose(), delay);
      return () => clearTimeout(timer);
    }
  }, [error, delay, handleClose]);

  const { errorMsg, isError } = error || {};

  return (
    <div
      className={clx(
        "fixed top-10 left-[50%] translate-x-[-50%] z-[1200] w-[300px] duration-500",
        isError ? "top-10" : "top-[-1000px]"
      )}
    >
      <button onClick={handleClose}>
        <div role="alert" className="text-white rounded alert alert-error">
          <MdErrorOutline className="w-5 h-5" />
          <span>Error! {errorMsg || "An error occurred."}</span>
        </div>
      </button>
    </div>
  );
};

export default ErrorAlert;
