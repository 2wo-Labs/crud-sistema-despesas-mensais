import unittest
from unittest.mock import patch
from io import StringIO
import sys
from datetime import datetime
import pandas as pd

import main

from projeto import (
    adicionar_despesa,
    editar_despesa,
    excluir_despesa,
    filtrar_despesas,
    gerar_estatisticas,
)


class TestProjetoGestao(unittest.TestCase):
    def setUp(self):
        self.gastos_csv_data = "Descrição,Valor,Data,Categoria\n"
        self.gastos_csv_data += "Comida,15.50,2023-01-05,Alimentação\n"
        self.gastos_csv_data += "Transporte,5.00,2023-01-10,Transporte\n"
        self.gastos_csv_data += "Cinema,25.00,2023-02-15,Lazer\n"

        self.mock_input_data = ["Cinema", "30.00", "2023-02-15", "Lazer"]

    def test_adicionar_despesa(self):
        with patch("builtins.open", return_value=StringIO()) as mock_file:
            adicionar_despesa(*self.mock_input_data)
            mock_file.return_value.write.assert_called_once_with(
                ",".join(self.mock_input_data) + "\n"
            )

    def test_editar_despesa(self):
        with patch(
            "builtins.open", return_value=StringIO(self.gastos_csv_data)
        ) as mock_file:
            with patch("csv.writer") as mock_writer:
                editar_despesa(1, *self.mock_input_data)
                rows = mock_file.return_value.readlines()
                rows[1] = ",".join(self.mock_input_data) + "\n"
                mock_writer.return_value.writerows.assert_called_once_with(
                    [row.strip().split(",") for row in rows]
                )

    def test_excluir_despesa(self):
        with patch(
            "builtins.open", return_value=StringIO(self.gastos_csv_data)
        ) as mock_file:
            with patch("csv.writer") as mock_writer:
                excluir_despesa(1)
                rows = mock_file.return_value.readlines()
                del rows[1]
                mock_writer.return_value.writerows.assert_called_once_with(
                    [row.strip().split(",") for row in rows]
                )

    def test_filtrar_despesas(self):
        expected_output = [
            {
                "Descrição": "Cinema",
                "Valor": "25.00",
                "Data": "15/02/2023",
                "Categoria": "Lazer",
            }
        ]
        with patch("builtins.open", return_value=StringIO(self.gastos_csv_data)):
            output = filtrar_despesas("02", "Lazer")
            self.assertEqual(output, expected_output)

    def test_gerar_estatisticas(self):
        with patch("builtins.open", return_value=StringIO(self.gastos_csv_data)):
            with patch("streamlit.write"):
                with patch("matplotlib.pyplot.subplots") as mock_subplots:
                    mock_ax = mock_subplots.return_value.__enter__.return_value
                    gerar_estatisticas()
                    mock_ax.pie.assert_called_once()

    @patch("streamlit.text_input")
    @patch("streamlit.number_input")
    @patch("streamlit.date_input")
    @patch("streamlit.selectbox")
    def test_main_adicionar_despesa(
        self, mock_selectbox, mock_date_input, mock_number_input, mock_text_input
    ):
        mock_selectbox.return_value = "Adicionar Despesa"
        mock_text_input.return_value = "Comida"
        mock_number_input.return_value = 15.50
        mock_date_input.return_value = datetime(2023, 1, 5).date()
        expected_output = "Descrição: Comida\nValor: R$ 15.50\nData: 2023-01-05\nCategoria: Alimentação\n"
        with patch("builtins.open", return_value=StringIO()):
            with patch("streamlit.button", return_value=True):
                with patch("streamlit.success") as mock_success:
                    with patch("streamlit.write") as mock_write:
                        main()
                        mock_success.assert_called_once()
                        mock_write.assert_called_with(expected_output)

    @patch("streamlit.selectbox")
    def test_main_visualizar_despesas(self, mock_selectbox):
        mock_selectbox.return_value = "Visualizar Despesas"
        expected_output = [
            {
                "Descrição": "Comida",
                "Valor": "15.50",
                "Data": "05/01/2023",
                "Categoria": "Alimentação",
            },
            {
                "Descrição": "Transporte",
                "Valor": "5.00",
                "Data": "10/01/2023",
                "Categoria": "Transporte",
            },
            {
                "Descrição": "Cinema",
                "Valor": "25.00",
                "Data": "15/02/2023",
                "Categoria": "Lazer",
            },
        ]
        with patch("builtins.open", return_value=StringIO(self.gastos_csv_data)):
            with patch("streamlit.button", return_value=True):
                with patch("streamlit.table") as mock_table:
                    main()
                    mock_table.assert_called_once_with(expected_output)


if __name__ == "__main__":
    unittest.main()
