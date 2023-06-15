# Sistema de Gastos Mensais

## Descrição do Projeto
O Sistema de Gastos Mensais é uma aplicação simples desenvolvida utilizando o Streamlit. Ele permite aos usuários registrar, editar, excluir e visualizar despesas mensais. Os dados são salvos localmente em um arquivo CSV. Além disso, o sistema oferece funcionalidades de análise de dados, incluindo estatísticas e visualizações gráficas dos gastos por categoria e ao longo do tempo.

## Funcionalidades

- Adicionar despesas: Os usuários podem inserir os detalhes de uma nova despesa, como descrição, valor, data e categoria. Os dados são salvos no arquivo CSV local.

- Editar despesas: Os usuários podem selecionar uma despesa existente da lista e fazer alterações nos detalhes, como descrição, valor, data ou categoria. As alterações são atualizadas no arquivo CSV.

- Excluir despesas: Os usuários podem selecionar uma despesa da lista e removê-la. A despesa é removida do arquivo CSV.

- Visualizar despesas: Os usuários podem filtrar e visualizar as despesas por mês ou categoria. O sistema exibe os dados correspondentes na interface do Streamlit.


## Como Executar

1. Certifique-se de ter o Python 3.7 ou superior instalado.

2. Clone o repositório para o seu ambiente local.
```
git clone git@github.com:2wo-Labs/crud-sistema-gastos-mensais.git
```

3. Instale as dependências usando o comando:
```
pip install -r requirements.txt
```

4. Execute o aplicativo utilizando o comando:
```
streamlit run app.py
```

5. O aplicativo será aberto em seu navegador padrão. Você pode interagir com as diferentes funcionalidades do sistema.

## Dependências

O sistema depende das seguintes bibliotecas Python:

- pandas
- matplotlib
- chardet
- streamlit

Você pode instalá-las manualmente ou usando o arquivo `requirements.txt` fornecido.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias ou correções.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
