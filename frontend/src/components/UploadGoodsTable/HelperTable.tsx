import { Button, Space, Input, Checkbox } from "antd";
import { FilterDropdownProps } from "antd/lib/table/interface";

const TableHelper = {
  getStringListColumnSearchProps: (dataIndex: string, dataSource: any[]) => {
    let values: string[] = [];
    let filter = "";
    let prevVisible = false;

    return {
      filterDropdown: (params: FilterDropdownProps) => {
        const {
          setSelectedKeys,
          selectedKeys,
          confirm,
          clearFilters,
          visible,
        } = params;

        if (prevVisible !== visible && visible) {
          filter = "";
          values = Array.from(
            new Set((dataSource || []).map((x) => x[dataIndex]).sort())
          );
        }
        prevVisible = visible;
        const visibleValues = values.filter((x) =>
          filter && x ? x.toLowerCase().includes(filter.toLowerCase()) : true
        );

        return (
          <div style={{ padding: 8 }}>
            <Space>
              <Input
                placeholder="Фильтр"
                value={filter}
                onChange={(e) => {
                  filter = e.target.value;
                  setSelectedKeys([]);
                }}
                style={{ width: 188 }}
              />
              <Button
                onClick={() => setSelectedKeys(visibleValues)}
                size="small"
                title="Выделить все"
              >
                V
              </Button>
              <Button
                onClick={() => setSelectedKeys([])}
                size="small"
                title="Снять выделение"
              >
                X
              </Button>
            </Space>
            <Checkbox.Group
              options={visibleValues
                .sort()
                .map((x) => ({
                  label: x || "Пустое значение",
                  value: x || "",
                }))}
              value={selectedKeys as any}
              onChange={(e) => setSelectedKeys(e as any)}
              className="table-filter-checkbox-group"
            />
            <Space>
              <Button
                type="primary"
                onClick={() => confirm()}
                size="small"
                style={{ width: 90 }}
              >
                Искать
              </Button>
              <Button
                onClick={() => TableHelper.handleReset(clearFilters, confirm)}
                size="small"
                style={{ width: 90 }}
              >
                Сбросить
              </Button>
            </Space>
          </div>
        );
      },
      onFilter: (value: any, record: any) =>
        record[dataIndex]?.toString().toLowerCase() ===
        value?.toString().toLowerCase(),
    };
  },
  handleReset: (clearFilters: VoidFunction | undefined, confirm: Function) => {
    if (clearFilters) clearFilters();
    confirm();
  },
};

export default TableHelper;
