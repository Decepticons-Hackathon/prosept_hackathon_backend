import React, { useState } from "react";
import type { TableProps } from "antd";
import { Button, Space, Table } from "antd";
import styles from "./UploadGoodsTable.module.scss";
import { ParsingType } from "../Matching/Matching";

import type {
  ColumnsType,
  FilterValue,
  SorterResult,
} from "antd/es/table/interface";
import TableHelper from "./HelperTable";

type UploadGoodsTableProps = {
  parsingData: ParsingType[];
  onUploadSelectClick: (index: number) => void;
  selectedLineUploadGoods: string | null;
};

const UploadGoodsTable: React.FC<UploadGoodsTableProps> = ({
  parsingData,
  onUploadSelectClick,
  selectedLineUploadGoods,
}) => {
  const [filteredInfo, setFilteredInfo] = useState<
    Record<string, FilterValue | null>
  >({});
  const [sortedInfo, setSortedInfo] = useState<SorterResult<ParsingType>>({});

  console.log("UploadGoodsTable, onUploadSelectClick:", onUploadSelectClick);

  const onLineClick = (record: ParsingType) => {
    const index = parseInt(record.key, 10);
    console.log("onLineClick вызвана, индекс:", index);
    onUploadSelectClick(index);
  };
  const handleChange: TableProps<ParsingType>["onChange"] = (
    pagination,
    filters,
    sorter
  ) => {
    console.log("Various parameters", pagination, filters, sorter);
    setFilteredInfo(filters);
    setSortedInfo(sorter as SorterResult<ParsingType>);
  };

  const clearFilters = () => {
    setFilteredInfo({});
  };

  const columns: ColumnsType<ParsingType> = [
    {
      title: "URL",
      dataIndex: "product_url",
      key: "product_url",
      ...TableHelper.getStringListColumnSearchProps("product_url", parsingData),
      width: "12%",
      render: (text) => {
        const match = text.match(/https?:\/\/(?:www\.)?([^\/.]+)\./);
        const displayText = match ? match[1] : text;
        return (
          <a href={text} target="_blank" rel="noopener noreferrer">
            {displayText}
          </a>
        );
      },

      // sorter: (a, b) => a.suggestion.length - b.suggestion.length,
      // sortOrder:
      //   sortedInfo.columnKey === "suggestion" ? sortedInfo.order : null,
      // ellipsis: true,
    },

    {
      title: "Дата",
      dataIndex: "date",
      key: "date",
      ...TableHelper.getStringListColumnSearchProps("date", parsingData),
      width: "13%",

      // sorter: (a, b) => a.suggestion.length - b.suggestion.length,
      // sortOrder:
      //   sortedInfo.columnKey === "suggestion" ? sortedInfo.order : null,
      // ellipsis: true,
    },

    {
      title: "Цена",
      dataIndex: "price",
      key: "price",
      ...TableHelper.getStringListColumnSearchProps("price", parsingData),
      width: "11%",
      // sorter: (a, b) => a.suggestion.length - b.suggestion.length,
      // sortOrder:
      //   sortedInfo.columnKey === "suggestion" ? sortedInfo.order : null,
      // ellipsis: true,
    },

    {
      title: "Статус",
      dataIndex: "status",
      key: "status",
      ...TableHelper.getStringListColumnSearchProps("status", parsingData),
      width: "13%",
      // sorter: (a, b) => a.suggestion.length - b.suggestion.length,
      // sortOrder:
      //   sortedInfo.columnKey === "suggestion" ? sortedInfo.order : null,
      // ellipsis: true,
    },

    {
      title: "Наименование товара",
      dataIndex: "product_name",
      key: "product_name",
      ...TableHelper.getStringListColumnSearchProps(
        "product_name",
        parsingData
      ),
      width: "48%",
      // sortOrder: sortedInfo.columnKey === "product" ? sortedInfo.order : null,
      ellipsis: true,
    },
  ];

  return (
    <div>
      <Space style={{ marginTop: 15 }}>
        <Button style={{ marginBottom: 15 }} onClick={clearFilters}>
          Сбросить фильтры
        </Button>
      </Space>
      <Table
        columns={columns}
        dataSource={parsingData}
        onChange={handleChange}
        size="small"
        pagination={{
          pageSize: 8,
        }}
        bordered
        onRow={(record) => ({
          onClick: () => {
            //@ts-ignore
            onUploadSelectClick(record.key);
          },
        })}
        rowClassName={(record) =>
          //@ts-ignore
          record.key === selectedLineUploadGoods ? styles.selectedLine : ""
        }
      />
    </div>
  );
};

export default UploadGoodsTable;
