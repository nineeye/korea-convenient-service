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


    products = db["products"]


    brands = []



    for product in products:


        name = product.get(
            "clean_name",
            ""
        )


        if not name:
            continue



        words = name.split()



        if words:

            brand = words[0]

            brands.append(
                brand
            )



    counter = Counter(
        brands
    )



    print("===================")

    print("브랜드 TOP20")

    print("===================")



    for brand,count in counter.most_common(20):

        print(
            count,
            "개 :",
            brand
        )



if __name__ == "__main__":

    run()
