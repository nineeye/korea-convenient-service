import json
import re
from datetime import datetime


MASTER_DB = "../data/master_db.json"

RULE_FILE = "../rules/normalize_rules.json"



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(path, data):

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



def normalize_name(name, rules):


    result = name



    # -------------------
    # 단어 제거
    # -------------------

    for word in rules["remove_words"]:

        result = result.replace(
            word,
            ""
        )



    # -------------------
    # 패턴 제거
    # -------------------

    for pattern in rules["remove_patterns"]:

        result = re.sub(
            pattern,
            "",
            result
        )



    # -------------------
    # 빈 괄호 제거
    # -------------------

    result = re.sub(
        r"\(\s*\)",
        "",
        result
    )



    # -------------------
    # 특수문자 정리
    # -------------------

    result = re.sub(
        r"[,\|]+",
        " ",
        result
    )



    # x 단독 제거
    result = re.sub(
        r"\bx\b",
        " ",
        result,
        flags=re.IGNORECASE
    )



    # -------------------
    # 여러 공백 정리
    # -------------------

    result = re.sub(
        r"\s+",
        " ",
        result
    )



    # -------------------
    # 앞뒤 특수문자 제거
    # -------------------

    result = re.sub(
        r"^[^가-힣a-zA-Z0-9]+",
        "",
        result
    )


    result = re.sub(
        r"[^가-힣a-zA-Z0-9]+$",
        "",
        result
    )


    # 남은 괄호 제거
result = re.sub(
    r"[\(\)]",
    "",
    result
)


# 숫자만 남은 조각 제거
result = re.sub(
    r"\s+\d+$",
    "",
    result
)



    return result.strip()





def run():


    db = load_json(
        MASTER_DB
    )


    rules = load_json(
        RULE_FILE
    )


    count = 0



    for product in db["products"]:


        original = product["original_name"]



        clean = normalize_name(
            original,
            rules
        )


        product["clean_name"] = clean


        count += 1




    db["meta"]["last_update"] = datetime.now().strftime("%Y-%m-%d")


    save_json(
        MASTER_DB,
        db
    )



    print("===================")

    print("정규화 완료")

    print(
        "처리 상품:",
        count
    )

    print("===================")





if __name__ == "__main__":

    run()
