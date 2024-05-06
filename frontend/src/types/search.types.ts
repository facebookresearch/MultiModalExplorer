// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

export type SearchResponseProps = {
  data:
    | {
        index: string;
        data: string;
        media_type: string;
      }[]
    | null;
  setData: (e) => void;
  isPending: boolean;
  postData: (e) => void;
};
