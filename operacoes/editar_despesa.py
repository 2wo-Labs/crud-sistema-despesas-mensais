import csv


def editar_despesa(index, descricao, valor, data, categoria):
    with open("../gastos.csv", "r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
        file.close()

    rows[index] = [descricao, valor, data, categoria]

    with open("gastos.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        file.close()
