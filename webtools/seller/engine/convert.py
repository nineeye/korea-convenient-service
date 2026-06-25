import json
import os
from datetime import datetime


RAW_FOLDER = "../data/raw"
OUTPUT_FILE = "../data/master_db.json"


def create_product(product_id, category, name):

    return {

        "id": product_id,

        "category": category,

        "keyword": category,


        "original_name": name,


        "clean_name": "",


        "brand": "",


        "attributes": {},


        "removed_words": [],


        "duplicate_count": 0,


        "status": "new",


        "history": [

            {

                "date": datetime.now().strftime("%Y-%m-%d"),

                "action": "added"

            }

        ]

    }



def convert():


    products = []

    product_id = 1



    files = os.listdir(RAW_FOLDER)



    for file in files:


        if not file.endswith(".json"):

            continue



        category = file.replace(".json","")


        path = os.path.join(
            RAW_FOLDER,
            file
        )



        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:


            data = json.load(f)



        print(
            f"{file} 불러오는중..."
        )



        for name in data:



            product = create_product(

                product_id,

                category,

                name

            )


            products.append(product)


            product_id += 1




    master = {


        "meta":{


            "version":"1.0",


            "total_products":len(products),


            "last_update":
            datetime.now().strftime("%Y-%m-%d")


        },


        "products":products


    }



    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as f:



        json.dump(

            master,

            f,

            ensure_ascii=False,

            indent=2

        )



    print("===================")

    print("완료")

    print(
        "총 상품:",
        len(products)
    )

    print("===================")



if __name__=="__main__":

    convert()
