// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import axios from "axios";

import { BASE_URL } from "@constants";

export const getEmbeddingPoints = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/embedding/get_embeddings`);

    return response?.data?.data || [];
  } catch (error) {
    throw new Error(error as string);
  }
};

export const getEmbeddingPointDetails = async (
  point: number[]
): Promise<{ id: number }> => {
  // This is currently a mock to simulate behavior for testing purposes.
  // TODO: Replace this mock with the real implementation once it's available.

  return new Promise((resolve, reject) => {
    try {
      setTimeout(() => {
        resolve({ id: point[0] });
      }, 2000);
    } catch (error) {
      reject(error);
    }
  });
};
