import streamlit as st
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import chardet


CATEGORIAS = [
    "Alimentação",
    "Transporte",
    "Lazer",
    "Saúde",
    "Educação",
    "Viagem",
    "Outros Pagamentos",
]

MESES = {
    "Janeiro": "01", 
    "Fevereiro": "02",
    "Março": "03",
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12",
}

# Função para formatar a data
def formatar_data(data):
    dia, mes, ano = data.split("/")
    return f"{dia}/{MESES[mes]}/{ano}"

def adicionar_despesa(descricao, valor, data, categoria):
    with open("gastos.csv", "a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([descricao, valor, data, categoria])


def editar_despesa(index, descricao, valor, data, categoria):
    with open("gastos.csv", "r", newline="", encoding='utf-8') as file:
        rows = list(csv.reader(file))
    rows[index] = [descricao, valor, data, categoria]
    with open("gastos.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def excluir_despesa(index):
    with open("gastos.csv", "r", newline="", encoding='utf-8') as file:
        rows = list(csv.reader(file))
    del rows[index]
    with open("gastos.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def filtrar_despesas(mes, categoria):
    with open('gastos.csv', 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']

    with open('gastos.csv', 'r', newline='', encoding=encoding) as file:
        reader = csv.reader(file)
        rows = list(reader)

    df = pd.DataFrame(rows, columns=['Descrição', 'Valor', 'Data', 'Categoria'])
    df['Data'] = pd.to_datetime(df['Data'])

    if mes:
        df = df[df['Data'].dt.month == int(mes)]
    if categoria:
        df = df[df['Categoria'] == categoria]

    if not df.empty:
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
        df = df.rename(columns={'Descrição': 'Descrição', 'Valor': 'Valor', 'Data': 'Data', 'Categoria': 'Categoria'})
        return df.to_dict('records')

    return []


def gerar_estatisticas():
    with open('gastos.csv', 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']

    with open('gastos.csv', 'r', newline='', encoding=encoding) as file:
        reader = csv.reader(file)
        rows = list(reader)
    df = pd.DataFrame(rows, columns=['Descrição', 'Valor', 'Data', 'Categoria'])
    df['Valor'] = df['Valor'].astype(float)
    valores = [float(row[1]) for row in rows]
    total = sum(valores)
    media = total / len(valores)
    maior_valor = max(valores)

    st.subheader('Total de Gastos')
    total = df['Valor'].sum()
    menor_valor = min(valores)
    st.write(f'Total: R$ {total:.2f}')
    st.write(f'Média: R$ {media:.2f}')
    st.write(f'Maior valor: R$ {maior_valor:.2f}')
    st.write(f'Menor valor: R$ {menor_valor:.2f}')

    st.subheader('Gastos por Categoria')
    gastos_por_categoria = df.groupby('Categoria')['Valor'].sum()
    st.bar_chart(gastos_por_categoria)

    st.subheader('Média de Gastos por Categoria')
    media_por_categoria = df.groupby('Categoria')['Valor'].mean()
    st.bar_chart(media_por_categoria)

    st.subheader('Visualização dos Gastos por Categoria')
    fig, ax = plt.subplots()
    ax.pie(gastos_por_categoria, labels=gastos_por_categoria.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)




def main():
    st.title("Sistema de Gastos Mensais")

    opcoes = [
        "Adicionar Despesa",
        "Editar Despesa",
        "Excluir Despesa",
        "Visualizar Despesas",
        "Análise Exploratória",
    ]
    escolha = st.sidebar.selectbox("Selecione uma opção", opcoes)

    if escolha == "Adicionar Despesa":
        st.header("Adicionar Despesa")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", step=0.01, format="%.2f")
        data = st.date_input("Data")
        categoria = st.selectbox("Categoria", CATEGORIAS)
        if st.button("Adicionar"):
            adicionar_despesa(descricao, valor, data, categoria)
            st.success("Despesa adicionada com sucesso!")

    elif escolha == "Editar Despesa":
        st.header("Editar Despesa")
        with open("gastos.csv", "r", newline="") as file:
            reader = csv.reader(file)
            despesas = list(reader)
        if despesas:
            selected_index = st.selectbox(
                "Selecione uma despesa para editar", range(len(despesas))
            )
            descricao = st.text_input("Descrição", value=despesas[selected_index][0])
            valor = st.number_input(
                "Valor",
                step=0.01,
                format="%.2f",
                value=float(despesas[selected_index][1]),
            )
            data_visual = datetime.strptime(despesas[selected_index][2], '%Y-%m-%d').date()
            data = st.date_input("Data", value=data_visual)
            categoria = st.selectbox(
                "Categoria",
                CATEGORIAS,
                index=CATEGORIAS.index(despesas[selected_index][3]),
            )
            if st.button("Salvar"):
                editar_despesa(selected_index, descricao, valor, data, categoria)
                st.success("Despesa editada com sucesso!")
        else:
            st.warning("Nenhuma despesa encontrada!")

    elif escolha == "Excluir Despesa":
        st.header("Excluir Despesa")
        with open("gastos.csv", "r", newline="") as file:
            reader = csv.reader(file)
            despesas = list(reader)
        if despesas:
            selected_index = st.selectbox(
                "Selecione uma despesa para excluir", range(len(despesas))
            )
            descricao = despesas[selected_index][0]
            valor = despesas[selected_index][1]
            data = despesas[selected_index][2]
            categoria = despesas[selected_index][3]
            st.write(f"Descrição: {descricao}")
            st.write(f"Valor: R$ {valor}")
            st.write(f"Data: {data}")
            st.write(f"Categoria: {categoria}")
            if st.button("Excluir"):
                excluir_despesa(selected_index)
                st.success("Despesa excluída com sucesso!")
        else:
            st.warning("Nenhuma despesa encontrada!")

    elif escolha == "Visualizar Despesas":
        st.header("Visualizar Despesas")
        with open("gastos.csv", "r", newline="") as file:
            reader = csv.reader(file)
            despesas = list(reader)
        if despesas:
            mes = st.selectbox(
                "Filtrar por mês",
                ["", *[nome for nome in MESES.keys()]],
            )
            categoria = st.selectbox(
                "Filtrar por categoria",
                ["", *CATEGORIAS],
            )
            rows = filtrar_despesas(MESES.get(mes), categoria)
            if rows:
                st.table(rows)
            else:
                st.warning("Nenhuma despesa encontrada com os filtros selecionados!")
        else:
            st.warning("Nenhuma despesa encontrada!")

    elif escolha == "Análise Exploratória":
        st.header("Análise Exploratória de Dados")
        gerar_estatisticas()


if __name__ == "__main__":
    main()
