import React, { useState } from "react";
import { AutoComplete, Input } from "antd";
import { productsMap } from "../Matching/Matching";

interface AutoSearchProps {
  onAddToRecommendations: (item: string) => void;
}

const AutoSearch: React.FC<AutoSearchProps> = ({ onAddToRecommendations }) => {
  const [key, setKey] = useState(Math.random());
  const searchResult = (query: string) =>
    Object.entries(productsMap)
      .filter(([, description]) =>
        //@ts-ignore
        description.toLowerCase().includes(query.toLowerCase())
      )
      .map(([key, description]) => ({
        value: description,
        label: (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>{description as string}</span>
          </div>
        ),
      }));

  const [options, setOptions] = useState("");

  const handleSearch = (value: string) => {
    //@ts-ignore
    setOptions(value ? searchResult(value) : []);
  };

  const onSelect = (value: string) => {
    console.log("onSelect", value);
    onAddToRecommendations(value);
    setKey(Math.random());
  };

  return (
    <AutoComplete
      key={key}
      popupMatchSelectWidth={600}
      style={{ width: 600 }}
      //@ts-ignore
      options={options}
      onSelect={onSelect}
      onSearch={handleSearch}
      size="large"
    >
      <Input.Search
        size="large"
        placeholder="Начните искать товар в каталоге Просепт"
        enterButton
      />
    </AutoComplete>
  );
};

export default AutoSearch;
