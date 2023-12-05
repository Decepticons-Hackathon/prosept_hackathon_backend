import { ProductModel } from "./ProductModel";

export type ProductListResult = {
  products: ProductModel[],
  products_count: number,
};
