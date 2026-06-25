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



    original_count = len(products)



    clean_names = []



    for p in products:


        name = p.get(
            "clean_name",
            ""
        )


        if name:

            clean_names.append(
                name
            )



    unique_count = len(
        set(clean_names)
    )



    duplicate_count = (
        original_count
        -
        unique_count
    )



    rate = round(
        duplicate_count / original_count * 100,
        2
    )



    counter = Counter(
        clean_names
    )



    print("===================")

    print("정규화 분석 결과")

    print("===================")

    print()

    print(
        "원본 상품수:",
        original_count
    )

    print(
        "정규화 상품수:",
        unique_count
    )

    print(
        "통합 가능:",
        duplicate_count
    )

    print(
        "압축률:",
        rate,
        "%"
    )



    print()

    print("===================")

    print("많이 나온 대표 상품명 TOP10")

    print("===================")



    for name,count in counter.most_common(10):

        print(
            count,
            "개 :",
            name
        )



if __name__ == "__main__":

    run()
