/**
 * (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.
 */

import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const getEmbeddingPoints = async (): Promise<
  Array<[number, number, number]>
> => {
  try {
    const response = await axios.get(`${BASE_URL}/embeddings`);
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
