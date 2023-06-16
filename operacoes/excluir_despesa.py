import csv


def excluir_despesa(index):
    with open("gastos.csv", "r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
        file.close()

    del rows[index]

    with open("gastos.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        file.close()
