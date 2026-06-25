import json
from collections import Counter


MASTER_DB = "../data/master_db.json"



KEYWORDS = [

    "오메가3",
    "비타민D",
    "루테인",
    "지아잔틴",
    "아스타잔틴",

    "유산균",
    "프로바이오틱스",
    "비피더스",

    "밀크씨슬",
    "실리마린",

    "홍삼",
    "진세노사이드",

    "알티지",
    "rTG",
    "식물성",
    "초임계",

    "키즈",
    "어린이",
    "임산부",
    "청소년",

    "면역",
    "장건강",
    "눈건강",
    "간건강",

    "프리미엄",
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


    result = {}



    for product in db["products"]:


        brand = product.get(
            "brand",
            "기타"
        )


        name = product.get(
            "clean_name",
            ""
        )


        if brand == "기타":

            continue



        if brand not in result:

            result[brand] = Counter()



        for keyword in KEYWORDS:


            if keyword.lower() in name.lower():

                result[brand][keyword] += 1





    print("===================")

    print("브랜드별 키워드 분석")

    print("===================")



    for brand,counter in sorted(
        result.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True
    )[:20]:


        print()

        print("###",brand)


        for keyword,count in counter.most_common(10):

            print(
                count,
                "개 :",
                keyword
            )





if __name__ == "__main__":

    run()
