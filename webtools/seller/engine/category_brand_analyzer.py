import json
from collections import Counter


MASTER_DB = "../data/master_db.json"



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def run():

    db = load_json(
        MASTER_DB
    )


    result = {}



    for product in db["products"]:


        category = product.get(
            "category",
            "기타"
        )


        brand = product.get(
            "brand",
            "기타"
        )


        if category not in result:

            result[category] = Counter()



        if brand:

            result[category][brand] += 1





    print("===================")

    print("카테고리별 브랜드 TOP")

    print("===================")



    for category,counter in result.items():


        print()

        print("###", category)


        for brand,count in counter.most_common(10):

            print(
                count,
                "개 :",
                brand
            )





if __name__ == "__main__":

    run()
