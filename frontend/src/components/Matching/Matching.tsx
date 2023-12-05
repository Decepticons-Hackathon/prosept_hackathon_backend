import GradientButton from "../GradientButton/GradientButton";
import styles from "./Matching.module.scss";
import jsonData from "../../../public/response_list.json";
import responseForMatching from "../../../public/response_product-to-matched-list_all.json";
import AutoSearch from "../AutoSearch/AutoSearch";
import { useState } from "react";
import RecommendationsTable from "../RecommendationsTable/RecommendationsTable";
import UploadGoodsTable from "../UploadGoodsTable/UploadGoodsTable";

export const productsMap: any = {};

jsonData.data.products.forEach((product: any, index: number) => {
  productsMap[index] = product.name_1c;
});

//@ts-ignore
const parsing: ParsingType[] = responseForMatching.data.dealer_products.map(
  //@ts-ignore
  (item, index) => ({
    key: index,
    date: item.dealer_product.date,
    status: item.dealer_product.dealer_product_status.status,
    price: item.dealer_product.price,
    product_name: item.dealer_product.product_name,
    product_url: item.dealer_product.product_url,
    //@ts-ignore
    procreator_variants: item.procreator_variants.map((variant) => ({
      product_id: variant.product_id,
      name_1c: variant.name_1c,
    })),
  })
);

type ProcreatorVariantType = {
  product_id: number;
  name_1c: string;
};

export type ParsingType = {
  key: string;
  product_name: string;
  price: number;
  product_url: string;
  date: string;
  status: string;
  procreator_variants: ProcreatorVariantType[];
};

//@ts-ignore
const dealerProducts = responseForMatching.data.dealer_products;

//@ts-ignore
const groupedRecommendations = dealerProducts.map((item, index) => ({
  key: index,
  //@ts-ignore
  variants: item.procreator_variants.map((variant) => ({
    product_id: variant.product_id,
    name: variant.name_1c,
  })),
}));

const Matching: React.FC = () => {
  const [isBtnsActive, setIsBtnsActive] = useState(false);
  const [recommendationsData, setRecommendationsData] = useState([]);
  const [parsingData, setParsingData] = useState<ParsingType[]>(parsing);

  const [selectedLineUploadGoods, setSelectedLineUploadGoods] = useState<
    string | null
  >(null);
  const [selectedLineRecommenadtions, setSelectedLineRecommenadtions] =
    useState<string | null>(null);
  const [approvedItems, setApprovedItems] = useState([]);
  const [holdOverdItems, setholdOverdItems] = useState([]);
  const [rejectedItems, setRejectedItems] = useState([]);

  const activeBtns = (isSelected: boolean) => {
    setIsBtnsActive(isSelected);
  };

  const onUploadSelectClick = (index: number) => {
    const selectedGroup = groupedRecommendations[index];

    //@ts-ignore
    const newRecommendations = selectedGroup.variants.map((variant) => {
      return {
        key: variant.product_id.toString(),
        name: variant.name,
      };
    });
    //@ts-ignore
    setSelectedLineUploadGoods(index);
    setRecommendationsData(newRecommendations);
  };

  const onRecommendationsClick = (key: string) => {
    setSelectedLineRecommenadtions(key);
  };

  const approveBtnClick: any = () => {
    const selectedUploadGoodsItem = parsingData.find(
      //@ts-ignore
      (item) => item.key === selectedLineUploadGoods
    );
    const selectedRecommendationItem = recommendationsData.find(
      //@ts-ignore
      (item) => item.key === selectedLineRecommenadtions
    );
    if (selectedUploadGoodsItem && selectedRecommendationItem) {
      const newItem = {
        uploadGoods: selectedUploadGoodsItem,
        recommendation: selectedRecommendationItem,
      };

      const updatedParsingData = parsingData.filter(
        //@ts-ignore
        (item) => item.key !== selectedLineUploadGoods
      );

      //@ts-ignore
      setParsingData(updatedParsingData);
      console.log(updatedParsingData);

      //@ts-ignore
      setApprovedItems((prevItems) => [...prevItems, newItem]);

      setSelectedLineUploadGoods(null);
      setSelectedLineRecommenadtions(null);
      setRecommendationsData([]);
    }
  };

  const holdOverBtnClick: any = () => {
    const selectedUploadGoodsItem = parsingData.find(
      //@ts-ignore
      (item) => item.key === selectedLineUploadGoods
    );
    const selectedRecommendationItem = recommendationsData.find(
      //@ts-ignore
      (item) => item.key === selectedLineRecommenadtions
    );
    if (selectedUploadGoodsItem && selectedRecommendationItem) {
      const newItem = {
        uploadGoods: selectedUploadGoodsItem,
        recommendation: selectedRecommendationItem,
      };

      // const updatedParsingData = parsingData.filter(
      //   //@ts-ignore
      //   (item) => item.key !== selectedLineUploadGoods
      // );

      const updatedParsingData = parsingData.map((item) => {
        if (item.key === selectedLineUploadGoods) {
          return { ...item, status: "hold over" };
        }
        return item;
      });

      //@ts-ignore
      setParsingData(updatedParsingData);
      // console.log(updatedParsingData);

      //@ts-ignore
      setholdOverdItems((prevItems) => [...prevItems, newItem]);

      setSelectedLineUploadGoods(null);
      setSelectedLineRecommenadtions(null);
      setRecommendationsData([]);
    }
  };

  const rejectBtnClick: any = () => {
    const selectedGood = parsingData.find(
      (item) => item.key === selectedLineUploadGoods
    );

    if (selectedGood) {
      const updatedParsingData = parsingData.map((item) =>
        item.key === selectedLineUploadGoods
          ? { ...item, status: "rejected" }
          : item
      );

      setParsingData(updatedParsingData);
      //@ts-ignore
      setRejectedItems((prevItems) => [
        ...prevItems,
        { ...selectedGood, status: "rejected" },
      ]);
      setRecommendationsData([]);
    }
  };

  const addToRecommendations = (itemName: string) => {
    const newRecommendation = {
      key: `${Date.now()}`,
      name: itemName,
    };

    //@ts-ignore
    setRecommendationsData((prev) => [...prev, newRecommendation]);
  };

  return (
    <div className={styles.table}>
      <div className={styles.goods}>
        <h3 className={styles.text}>Список загруженных товаров:</h3>
        <UploadGoodsTable
          onUploadSelectClick={onUploadSelectClick}
          selectedLineUploadGoods={selectedLineUploadGoods}
          parsingData={parsingData}
        />
      </div>
      <div className={styles.optionsContainer}>
        <div className={styles.search}>
          <AutoSearch onAddToRecommendations={addToRecommendations} />
        </div>
        <div className={styles.options}>
          <h3 className={styles.optionsText}>Окно предложенных вариантов</h3>
          <RecommendationsTable
            recommendationsData={recommendationsData}
            activeBtns={activeBtns}
            onRecommendationsClick={setSelectedLineRecommenadtions}
            selectedLineRecommenadtions={selectedLineRecommenadtions}
          />
        </div>
        <div className={styles.buttons}>
          <GradientButton onClick={approveBtnClick} disabled={!isBtnsActive}>
            Подтвердить
          </GradientButton>
          <GradientButton onClick={holdOverBtnClick} disabled={!isBtnsActive}>
            Отложить
          </GradientButton>
          <GradientButton
            disabled={recommendationsData.length === 0}
            onClick={rejectBtnClick}
          >
            Отклонить все
          </GradientButton>
        </div>
        <div className={styles.buttons}>
          {/* <button className={styles.historyBtn}>
            Посмотреть историю действий
          </button> */}
        </div>
      </div>
    </div>
  );
};

export default Matching;
