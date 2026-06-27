
import json
import re
from collections import Counter


MASTER_DB = "../data/master_db.json"



# 분석할 주요 키워드
KEYWORDS = [

    # 원료/성분
    "유산균",
    "프로바이오틱스",
    "비피더스",
    "밀크씨슬",
    "실리마린",
    "오메가3",
    "비타민D",
    "루테인",
    "지아잔틴",
    "아스타잔틴",
    "홍삼",
    "진세노사이드",


    # 특징
    "식물성",
    "rTG",
    "알티지",
    "초임계",
    "고함량",
    "프리미엄",
    "저분자",


    # 대상
    "어린이",
    "키즈",
    "임산부",
    "청소년",
    "여성",
    "남성",


    # 기능
    "장건강",
    "눈건강",
    "혈행",
    "면역",
    "간건강",
    "피로",
    "건강"
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


    counter = Counter()



    for product in db["products"]:


        name = product.get(
            "clean_name",
            ""
        )


        if not name:
            continue



        for keyword in KEYWORDS:


            if keyword.lower() in name.lower():

                counter[keyword] += 1





    print("===================")

    print("키워드 TOP")

    print("===================")



    for keyword,count in counter.most_common(30):

        print(
            count,
            "개 :",
            keyword
        )




if __name__ == "__main__":

    run()
