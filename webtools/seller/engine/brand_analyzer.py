import json
from collections import Counter


MASTER_DB = "../data/master_db.json"

BRAND_FILE = "../data/brand_dictionary.json"



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def save_json(path,data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )





def find_brand(name, brands):


    # 1단계 : 사전 검색

    for brand in brands:


        if brand.lower() in name.lower():

            return brand




    # 2단계 : 첫 단어 후보

    words = name.split()


    if words:


        first = words[0]


        # 숫자 제거

        if len(first) >= 2:

            return first





    return "기타"





def run():


    db = load_json(
        MASTER_DB
    )


    brand_data = load_json(
        BRAND_FILE
    )


    brands = brand_data["brands"]



    counter = Counter()



    for product in db["products"]:


        name = product.get(
            "clean_name",
            ""
        )


        brand = find_brand(
            name,
            brands
        )


        product["brand"] = brand


        counter[brand] += 1





    save_json(
        MASTER_DB,
        db
    )




    print("===================")

    print("브랜드 재분석 완료")

    print("===================")



    for brand,count in counter.most_common(20):

        print(
            count,
            "개 :",
            brand
        )





if __name__ == "__main__":

    run()
