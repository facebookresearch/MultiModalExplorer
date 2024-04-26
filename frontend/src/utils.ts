// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

export const clx = (...classes: string[]): string => {
  return classes.filter(Boolean).join(" ");
};

export const truncate = (str, len) =>
  str?.length
    ? str.length <= len
      ? `${str.slice(0, len)}`
      : `${str.slice(0, len)}...`
    : "";
