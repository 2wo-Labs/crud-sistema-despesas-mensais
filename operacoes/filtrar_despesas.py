import csv
import chardet
import pandas as pd


def filtrar_despesas(mes, categoria):
    with open("gastos.csv", "rb") as file:
        result = chardet.detect(file.read())
        file.close()
    encoding = result["encoding"]

    with open("gastos.csv", "r", newline="", encoding=encoding) as file:
        reader = csv.reader(file)
        rows = list(reader)
        file.close()

    df = pd.DataFrame(rows, columns=["Descrição", "Valor", "Data", "Categoria"])
    df["Data"] = pd.to_datetime(df["Data"], format="mixed")

    if mes:
        df = df[df["Data"].dt.month == int(mes)]
    if categoria:
        df = df[df["Categoria"] == categoria]

    if not df.empty:
        df["Data"] = df["Data"].dt.strftime("%d/%m/%Y")
        df = df.rename(
            columns={
                "Descrição": "Descrição",
                "Valor": "Valor",
                "Data": "Data",
                "Categoria": "Categoria",
            }
        )

        return df.to_dict("records")

    return []
