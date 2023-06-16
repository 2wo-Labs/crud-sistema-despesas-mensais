import csv


def adicionar_despesa(descricao, valor, data, categoria):
    with open("../gastos.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([descricao, valor, data, categoria])
        file.close()
