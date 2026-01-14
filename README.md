☀️ SunCare - Sistema de Gestão para Bronzeamento
Projeto desenvolvido para a disciplina de Programação Estruturada utilizando Python e Streamlit. O SunCare é uma solução completa para gerenciamento de espaços de bronzeamento, focando na segurança da cliente e na organização operacional.

🎯 Objetivo
Substituir agendas de papel e cronômetros manuais por um sistema digital unificado que gerencia cadastro, anamnese (saúde), agendamento e controle de tempo de exposição solar.

🛠️ Tecnologias Utilizadas
Python 3.10+
Streamlit: Framework para Interface Web Interativa.
Pandas: Manipulação de dados e tabelas.
Plotly: Biblioteca para gráficos dinâmicos e dashboards.
OpenPyXL: Suporte para operações com arquivos Excel.
Datetime: Lógica temporal e agendamentos.

🚀 Funcionalidades
Gestão de Clientes: Cadastro completo com ficha de saúde (anamnese) e alertas de risco.
Agendamento: Agenda visual com cálculo automático de término de sessão.
Mesa de Controle (Live):
Filtro automático de clientes do dia.
Cronômetros individuais em tempo real.
Controles rápidos (+5min, Pausa, Retomar).
Dashboard Financeiro:
Gráficos de faturamento por tipo de serviço.
Cálculo automático de Ticket Médio e receita total.
Extrato de lançamentos recentes.
Interface Premium: Design customizado via CSS (Paleta Gold/Champagne).

📦 Como Instalar e Rodar
Clone o repositório:

git clone [https://github.com/niedjalyvia-creator/projeto-suncare.git](https://github.com/niedjalyvia-creator/projeto-suncare.git)
cd projeto-suncare
Instale as dependências:

pip install -r requirements.txt
Execute a aplicação:

streamlit run SunCare.py

📂 Estrutura de Arquivos
SunCare.py: Arquivo principal (Interface Visual e Navegação).
banco.py: Módulo responsável pelo Banco de Dados (Salvar/Carregar).
regras.py: Módulo de Inteligência (Cálculos de agendamento e saúde).
dados_clientes.csv: Base de dados (gerado automaticamente pelo sistema).
requirements.txt: Lista de bibliotecas para instalação.
README.md: Documentação do projeto.

👥 Autores
Lyvia Niedja
Maria Clara
