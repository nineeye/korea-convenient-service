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


    candidates = []


    for p in db["products"]:


        if p.get("brand") == "기타":


            name = p.get(
                "clean_name",
                ""
            )


            words = name.split()



            if words:

                candidates.append(
                    words[0]
                )



    counter = Counter(
        candidates
    )



    print("===================")

    print("브랜드 후보 TOP30")

    print("===================")



    for name,count in counter.most_common(30):

        print(
            count,
            "개 :",
            name
        )



if __name__ == "__main__":

    run()
