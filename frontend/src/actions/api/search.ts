// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import axios from "axios";

import { BASE_URL } from "@constants";

export const getSearchQueryDetails = async (formData: {
  search_data: string;
  search_type: string;
}) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/search/search_data`,
      formData
    );
    return response?.data?.data || [];
  } catch (error) {
    throw new Error(error as string);
  }
};
