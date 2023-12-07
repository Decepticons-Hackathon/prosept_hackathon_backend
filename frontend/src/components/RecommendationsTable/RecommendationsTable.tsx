import React, { useState } from "react";
import type { TableProps } from "antd";
import { Button, Space, Table } from "antd";
import styles from "./RecommendationsTable.module.scss";
import { useEffect } from "react";

import type {
  ColumnsType,
  FilterValue,
  SorterResult,
} from "antd/es/table/interface";
import TableHelper from "../UploadGoodsTable/HelperTable";

type RecommendationsType = {
  key: string;
  name: string;
};

type RecommendationsTableProps = {
  recommendationsData: RecommendationsType[];
  activeBtns: (isSelected: boolean) => void;
  onRecommendationsClick: (key: string | null) => void;
  selectedLineRecommenadtions: string | null;
};

export const RecommendationsTable: React.FC<RecommendationsTableProps> = ({
  recommendationsData,
  activeBtns,
  onRecommendationsClick,
  selectedLineRecommenadtions,
}) => {
  const [filteredInfo, setFilteredInfo] = useState<
    Record<string, FilterValue | null>
  >({});
  const [sortedInfo, setSortedInfo] = useState<
    SorterResult<RecommendationsType>
  >({});

  const onLineClick = (record: RecommendationsType) => {
    onRecommendationsClick(record.key);
    activeBtns(true);
  };

  useEffect(() => {
    onRecommendationsClick(null);
    activeBtns(false);
  }, [recommendationsData]);

  const handleChange: TableProps<RecommendationsType>["onChange"] = (
    pagination,
    filters,
    sorter
  ) => {
    console.log("Various parameters", pagination, filters, sorter);
    setFilteredInfo(filters);
    setSortedInfo(sorter as SorterResult<RecommendationsType>);
  };

  const clearFilters = () => {
    setFilteredInfo({});
  };

  const columns: ColumnsType<RecommendationsType> = [
    {
      title: "Предлагаемое наименование товара",
      dataIndex: "name",
      key: "name",
      ...TableHelper.getStringListColumnSearchProps(
        "name",
        recommendationsData
      ),

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
        dataSource={recommendationsData}
        onChange={handleChange}
        size="small"
        pagination={{
          pageSize: 6,
        }}
        bordered
        onRow={(record) => ({
          onClick: () => onLineClick(record),
        })}
        rowClassName={(record) =>
          record.key === selectedLineRecommenadtions ? styles.selectedLine : ""
        }
      />
    </div>
  );
};

export default RecommendationsTable;
