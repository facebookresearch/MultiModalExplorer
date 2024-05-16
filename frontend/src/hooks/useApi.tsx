// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

/* eslint-disable @typescript-eslint/no-explicit-any */

import { useEffect, useState } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";

import { API_BASE_URL } from "@constants";
import { useAppContext } from "@providers/ContextProvider";

const errorHandler = (error: AxiosError): string => {
  if (error.response) {
    return `Server responded with error: ${error.response.status}`;
  } else if (error.request) {
    return `No response received: ${error.request}`;
  } else {
    return `Error occurred: ${error.message}`;
  }
};

export const useApiGetRequest = <T,>(path: string, params?: any) => {
  const [data, setData] = useState<T | null>(null);
  const [isPending, setIsPending] = useState<boolean>(false);

  const { setError } = useAppContext();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsPending(true);

        setError({
          isError: false,
          errorMsg: null,
        });

        const result: AxiosResponse = await axios({
          url: `${API_BASE_URL}/${path}`,
          method: "GET",
          params,
          headers: {
            "Content-Type": "application/json",
          },
        });
        setData(result?.data?.data);
      } catch (error) {
        const err = errorHandler(error as AxiosError);
        setError({
          isError: true,
          errorMsg: err,
        });
      } finally {
        setIsPending(false);
      }
    };

    fetchData();
  }, []);

  return { data, isPending };
};

export const useApiPostRequest = <T,>(path: string) => {
  const [data, setData] = useState<T | null>(null);
  const [isPending, setIsPending] = useState<boolean>(false);

  const { setError } = useAppContext();

  const postData = async (params?: any) => {
    try {
      setIsPending(true);

      setError({
        isError: false,
        errorMsg: null,
      });

      const result: AxiosResponse = await axios({
        url: `${API_BASE_URL}/${path}`,
        method: "POST",
        data: params,
        headers: {
          "Content-Type": "application/json",
        },
      });
      setData(result?.data?.data);
      return result?.data?.data;
    } catch (error) {
      const err = errorHandler(error as AxiosError);

      setError({
        isError: true,
        errorMsg: err,
      });
    } finally {
      setIsPending(false);
    }
  };

  return { data, setData, isPending, setIsPending, postData };
};
