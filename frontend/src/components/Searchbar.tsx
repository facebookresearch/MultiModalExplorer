// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { useState, ChangeEvent, KeyboardEvent, useRef } from "react";

import { getSearchQueryDetails } from "@actions/api/search";
import { useAppContext } from "@providers/ContextProvider";
import { clx } from "@utils";

import Search from "@assets/icons/search.svg?react";
import Cancel from "@assets/icons/cancel.svg?react";
import Caret from "@assets/icons/caret.svg?react";
import useOutsideClick from "@hooks/useClickOutside";

interface SearchResult {
  index: string;
  data: string;
  media_type: string;
}

const Searchbar: React.FC = () => {
  const { store } = useAppContext();

  const [searchInput, setSearchInput] = useState<string>("");
  const [searchQueryList, setSearchQueryList] = useState<SearchResult[] | null>(
    null
  );
  const [loadingSearchQuery, setLoadingSearchQuery] = useState<boolean>(false);
  const [showDropdown, setShowDropdown] = useState<boolean>(true);
  const [isSearching, setIsSearching] = useState<boolean>(false);

  const inputContainerRef = useRef<HTMLDivElement | null>(null);

  const dropdownRef = useOutsideClick(
    () => setShowDropdown(false),
    [inputContainerRef.current!]
  );

  const handleSearchQuery = async () => {
    setLoadingSearchQuery(true);
    setIsSearching(true);
    setShowDropdown(true);

    const details = await getSearchQueryDetails({
      search_data: searchInput,
      search_type: "text",
    });

    setSearchQueryList(details);
    setLoadingSearchQuery(false);
  };

  const handleInputKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSearchQuery();
    }
  };

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchInput(event.target.value);
  };

  const handleInputCancel = () => {
    setSearchInput("");
    setIsSearching(false);
    setSearchQueryList(null);
    store.handleZoomToOrigin();
  };

  return (
    <div className="relative h-full w-searchbar">
      <div
        ref={inputContainerRef}
        className="flex items-center justify-between w-full h-full px-4 border input-container border-neutral focus-within:border-neutral-content rounded-xl"
      >
        <div className="flex items-center flex-1 gap-2">
          <Search className="w-5 h-5" />
          <input
            className="w-full h-full py-4 bg-transparent outline-none"
            placeholder="Search ..."
            value={searchInput}
            onChange={handleInputChange}
            onKeyDown={handleInputKeyPress}
            onFocus={() => setShowDropdown(true)}
            disabled={loadingSearchQuery}
          />
        </div>
        <div className="flex items-center gap-2">
          {searchQueryList && (
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              disabled={loadingSearchQuery}
            >
              <Caret
                className={clx(
                  !showDropdown ? "rotate-0" : " rotate-180",
                  "w-7 h-7 cursor-pointer duration-300"
                )}
              />
            </button>
          )}
          {!!searchInput && (
            <button onClick={handleInputCancel} disabled={loadingSearchQuery}>
              <Cancel className="w-5 h-5 cursor-pointer" />
            </button>
          )}
        </div>
      </div>

      <div
        className={clx(
          isSearching && showDropdown ? "max-h-[350px]" : "max-h-0 invisible",
          "dropdown left-0 absolute top-20 w-full rounded-lg bg-base-200 z-[1000] duration-200 ease-in-out overflow-auto border border-neutral"
        )}
      >
        {loadingSearchQuery && <div className="p-4">Loading ...</div>}
        {!loadingSearchQuery && searchQueryList?.length === 0 && (
          <div className="p-4">No search results</div>
        )}
        {!loadingSearchQuery && searchQueryList?.length ? (
          <div ref={dropdownRef} className="dropdown-container">
            <ul role="list" className="p-4 divide-y divide-neutral">
              {searchQueryList.map((search) => (
                <li key={search.index} className="flex justify-between">
                  <div className="w-full p-4 duration-300 rounded-xl hover:bg-base-100">
                    <div
                      className="w-full h-full cursor-pointer text-start line-clamp-2"
                      onClick={() => {
                        store.handleZoomToPoint(parseInt(search.index));
                        setShowDropdown(false);
                      }}
                    >
                      {search.data}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default Searchbar;
