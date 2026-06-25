import json
from collections import Counter


MASTER_DB = "../data/master_db.json"



KEYWORDS = [

    # 성분
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


    # 특징
    "알티지",
    "rTG",
    "식물성",
    "초임계",
    "고함량",
    "프리미엄",


    # 대상
    "어린이",
    "키즈",
    "임산부",
    "청소년",


    # 기능
    "장건강",
    "눈건강",
    "간건강",
    "면역",
    "혈행"
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


    products = db["products"]



    categories = {}



    for product in products:


        category = product.get(
            "category",
            "기타"
        )


        name = product.get(
            "clean_name",
            ""
        )


        if not name:
            continue



        if category not in categories:

            categories[category] = Counter()



        for keyword in KEYWORDS:


            if keyword.lower() in name.lower():

                categories[category][keyword] += 1





    print("===================")

    print("카테고리별 키워드 분석")

    print("===================")



    for category, counter in categories.items():


        print()

        print("###", category)


        for keyword,count in counter.most_common(10):

            print(
                count,
                "개 :",
                keyword
            )



if __name__ == "__main__":

    run()
