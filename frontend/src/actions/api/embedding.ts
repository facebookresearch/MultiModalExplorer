// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { useApiGetRequest, useApiPostRequest } from "@hooks/useApi";

const apiGetRequest = useApiGetRequest;
const apiPostRequest = useApiPostRequest;

export const getEmbeddingPoints = () =>
  apiGetRequest("embedding/get_embeddings", {});

export const getEmbeddingPointDetails = () =>
  apiPostRequest("embedding/get_embeddings_details");
