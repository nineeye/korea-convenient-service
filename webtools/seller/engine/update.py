import json
import os
from datetime import datetime


MASTER_DB = "../data/master_db.json"


def load_master():

    with open(
        MASTER_DB,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_master(data):

    with open(
        MASTER_DB,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def update(new_file):


    master = load_master()


    products = master["products"]


    existing_names = set()


    for p in products:

        existing_names.add(
            p["original_name"]
        )


    new_count = 0

    duplicate_count = 0


    with open(
        new_file,
        "r",
        encoding="utf-8"
    ) as f:


        data = json.load(f)



    category = data["category"]

    titles = data["titles"]



    next_id = len(products)+1



    for title in titles:


        if title in existing_names:


            duplicate_count += 1


        else:


            product = {


                "id": next_id,

                "category": category,

                "keyword": category,

                "original_name": title,

                "clean_name": "",

                "brand": "",

                "attributes": {},

                "removed_words": [],

                "duplicate_count": 0,

                "status": "new",

                "history":[

                    {

                    "date":
                    datetime.now().strftime("%Y-%m-%d"),

                    "action":"added"

                    }

                ]

            }


            products.append(product)

            existing_names.add(title)


            next_id += 1

            new_count += 1



    master["meta"]["total_products"] = len(products)

    master["meta"]["last_update"] = datetime.now().strftime("%Y-%m-%d")


    save_master(master)



    print("===================")

    print("업데이트 완료")

    print()

    print("기존 DB :", len(products)-new_count)

    print("신규상품 :", new_count)

    print("중복상품 :", duplicate_count)

    print("현재 DB :", len(products))

    print("===================")



if __name__ == "__main__":


    file = input(
        "업데이트할 JSON 파일명 입력: "
    )


    update(
        "../data/raw/" + file
    )
