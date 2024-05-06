// Copyright (c) Meta Platforms, Inc. and affiliates.
//
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import { useState, ChangeEvent, KeyboardEvent, useRef } from "react";
import { RiSearchLine } from "react-icons/ri";
import { MdCancel } from "react-icons/md";
import { FaCaretDown } from "react-icons/fa6";

import { getSearchQueryDetails } from "@actions/api/search";
import { useAppContext } from "@providers/ContextProvider";
import useOutsideClick from "@hooks/useClickOutside";
import { clx } from "@utils";
import { SearchResponseProps } from "types/search.types";

const Searchbar: React.FC = () => {
  const { zoomHandlers } = useAppContext();

  const {
    data: searchQueryList,
    setData: setSearchQueryList,
    isPending: loadingSearchQuery,
    postData,
  } = getSearchQueryDetails() as SearchResponseProps;

  const [searchInput, setSearchInput] = useState<string>("");
  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  const inputContainerRef = useRef<HTMLDivElement | null>(null);

  const dropdownRef = useOutsideClick(
    () => setShowDropdown(false),
    [inputContainerRef.current!]
  );

  const handleSearchQuery = async () => {
    setShowDropdown(true);
    if (searchInput.length > 2) {
      await postData({
        search_data: searchInput,
        search_type: "text",
      });
    }
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
    setSearchQueryList(null);
    setShowDropdown(false);
    zoomHandlers.handleZoomToOrigin();
  };

  return (
    <div className="relative h-full w-searchbar">
      <div
        ref={inputContainerRef}
        className="relative flex items-center justify-between w-full h-full px-4 border input-container border-neutral focus-within:border-neutral-content rounded-xl"
      >
        <div className="flex items-center flex-1 gap-2">
          <RiSearchLine className="w-5 h-5" />
          <input
            className="w-full h-full py-4 bg-transparent outline-none"
            placeholder="Search ..."
            value={searchInput}
            onChange={handleInputChange}
            onKeyDown={handleInputKeyPress}
            disabled={loadingSearchQuery}
          />
        </div>
        <div className="flex items-center gap-2">
          {searchQueryList && (
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              disabled={loadingSearchQuery}
            >
              <FaCaretDown
                className={clx(
                  !showDropdown ? "rotate-0" : " rotate-180",
                  "w-5 h-5 duration-300"
                )}
              />
            </button>
          )}
          {!!searchInput && (
            <button onClick={handleInputCancel} disabled={loadingSearchQuery}>
              <MdCancel className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      <div
        className={clx(
          showDropdown ? "max-h-[350px]" : "max-h-0",
          "dropdown left-0 top-20 absolute w-full rounded-lg bg-base-200 z-[999] duration-200 transition-all overflow-auto"
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
                        zoomHandlers.handleZoomToPoint(parseInt(search.index));
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
