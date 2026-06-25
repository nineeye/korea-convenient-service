import json
from collections import Counter


MASTER_DB = "../data/master_db.json"


KEYWORDS = [

    "오메가3",
    "비타민D",
    "루테인",
    "유산균",
    "프로바이오틱스",
    "밀크씨슬",
    "홍삼",
    "알티지",
    "rTG",
    "초임계",
    "식물성",
    "프리미엄",
    "키즈",
    "임산부",
    "고함량"

]



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



    categories = {}



    for product in db["products"]:


        category = product.get(
            "category",
            "기타"
        )


        name = product.get(
            "clean_name",
            ""
        )


        brand = product.get(
            "brand",
            "기타"
        )



        if category not in categories:

            categories[category] = {

                "count":0,
                "brands":Counter(),
                "keywords":Counter()

            }



        categories[category]["count"] += 1


        categories[category]["brands"][brand]+=1



        for keyword in KEYWORDS:

            if keyword.lower() in name.lower():

                categories[category]["keywords"][keyword]+=1




    print("===================")

    print("시장 분석 리포트")

    print("===================")



    for category,data in categories.items():


        print()

        print("###",category)


        print(
            "총 상품:",
            data["count"]
        )


        print()

        print("TOP 브랜드")


        for b,c in data["brands"].most_common(5):

            print(
                c,
                "개 :",
                b
            )



        print()

        print("핵심 키워드")


        for k,c in data["keywords"].most_common(5):

            print(
                c,
                "개 :",
                k
            )





if __name__ == "__main__":

    run()
