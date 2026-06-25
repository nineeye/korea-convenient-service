import json
import os
from collections import Counter


MASTER_DB = "../data/master_db.json"

OUTPUT_FILE = "../data/analysis/category_keyword.json"



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
    "고함량",
    "프리미엄",

    "어린이",
    "키즈",
    "임산부",
    "청소년",

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




def save_json(path,data):

    folder = os.path.dirname(path)


    if not os.path.exists(folder):

        os.makedirs(folder)


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


        name = product.get(
            "clean_name",
            ""
        )


        if not name:
            continue



        if category not in result:

            result[category] = Counter()



        for keyword in KEYWORDS:


            if keyword.lower() in name.lower():

                result[category][keyword] += 1




    # Counter → 일반 dict 변환

    final = {}


    for category,counter in result.items():


        final[category] = dict(
            counter.most_common(30)
        )




    save_json(
        OUTPUT_FILE,
        final
    )



    print("===================")

    print("분석 저장 완료")

    print("===================")

    print(
        "파일:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    run()
