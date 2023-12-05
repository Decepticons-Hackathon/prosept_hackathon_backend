export type ProductModel = {
  product_id: number;
  article: string;
  ean_13: string;
  name: string;
  cost: number;
  min_rec_price: number | null;
  rec_price: number;
  category_id: number;
  ozon_name: string;
  name_1c: string;
  wb_name: string;
  ozon_article: string;
  wb_article: string;
  ym_article: string;
};
