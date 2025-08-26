
import pandas as pd
import sqlite3


def main():
    df = pd.read_csv("data/import_test.csv", sep=";")

    df["coeficiente"] = df["name"].apply(lambda x: x.split(" ")[-1])
    df["name"] = df["name"].apply(lambda x: " ".join(x.split(" ")[:-1]))

    df["coeficiente"] = df["coeficiente"].apply(lambda x: x.replace(",", "."))
    df["coeficiente"] = df["coeficiente"].astype(float)
    df["score"] = df["score"].astype(int)

    def get_probability(row):
        return row["coeficiente"] * row["score"]

    df["probability"] = df.apply(get_probability, axis=1)

    con = sqlite3.connect("datos_interview.db")

    cur = con.cursor()

    sql_create_table = """
    CREATE TABLE IF NOT EXISTS 
        datos(id INT,
            name VARCHAR(50),
            brand VARCHAR(50),
            score INT,
            probability REAL)
    """
    cur.execute(sql_create_table)

    sql_insert_table = """
    INSERT INTO datos (id, name, brand, score, probability)
    VALUES (?, ?, ?, ?, ?)
    """

    for _, row in df.iterrows():
        input_values = (
            row["id"],
            row["name"],
            row["brand"],
            row["score"],
            row["probability"]
        )
        cur.execute(sql_insert_table, input_values)

    con.commit()

    cur.execute("SELECT * FROM datos LIMIT 5")
    rows = cur.fetchall()

    for row in rows:
        print(row)
    con.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("error:", str(e))