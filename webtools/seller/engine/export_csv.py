import json
import csv


MASTER_DB = "../data/master_db.json"

OUTPUT_CSV = "../data/master_products.csv"



def export_csv():


    with open(
        MASTER_DB,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)



    products = data["products"]



    with open(

        OUTPUT_CSV,

        "w",

        encoding="utf-8-sig",

        newline=""

    ) as f:



        writer = csv.writer(f)



        writer.writerow([

            "ID",

            "카테고리",

            "원본상품명",

            "정규화상품명",

            "브랜드",

            "상태",

            "중복횟수"

        ])




        for p in products:


            writer.writerow([


                p["id"],


                p["category"],


                p["original_name"],


                p["clean_name"],


                p["brand"],


                p["status"],


                p["duplicate_count"]

            ])




    print("===================")

    print("CSV 생성 완료")

    print()

    print("파일:")

    print(OUTPUT_CSV)

    print()

    print("총 상품:" , len(products))

    print("===================")



if __name__ == "__main__":

    export_csv()
