import json
from collections import Counter


MASTER_DB = "../data/master_db.json"

GROUP_FILE = "../data/brand_group.json"



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)





def find_group(brand, groups):


    for group,brands in groups.items():

        if brand in brands:

            return group


    return brand





def run():


    db = load_json(
        MASTER_DB
    )


    groups = load_json(
        GROUP_FILE
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


        group = find_group(
            brand,
            groups
        )



        if category not in result:

            result[category] = Counter()



        result[category][group] += 1




    print("===================")

    print("브랜드 그룹 분석")

    print("===================")



    for category,counter in result.items():


        print()

        print("###",category)


        for brand,count in counter.most_common(10):

            print(
                count,
                "개 :",
                brand
            )





if __name__ == "__main__":

    run()
