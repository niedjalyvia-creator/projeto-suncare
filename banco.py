import pandas as pd
import os

ARQUIVO_AGENDA = 'dados_suncare.csv'
ARQUIVO_CLIENTES = 'clientes_cadastrados.csv'

# --- FUNÇÕES DA AGENDA ---
def carregar():
    if not os.path.exists(ARQUIVO_AGENDA):
        # Adicionamos 'Valor' nas colunas
        cols = ["Cliente", "Data", "Hora", "Pele", "Servico", "Tempo_Minutos", "Risco", "Valor", "Status"]
        df = pd.DataFrame(columns=cols)
        df.to_csv(ARQUIVO_AGENDA, index=False)
        return df
    return pd.read_csv(ARQUIVO_AGENDA)

def salvar(dado_novo):
    df = carregar()
    novo_df = pd.DataFrame([dado_novo])
    df = pd.concat([df, novo_df], ignore_index=True)
    df.to_csv(ARQUIVO_AGENDA, index=False)

# --- FUNÇÕES DE CLIENTES (COM ANAMNESE) ---
def carregar_clientes():
    if not os.path.exists(ARQUIVO_CLIENTES):
        # Adicionamos 'Anamnese' (Saúde) nas colunas
        cols = ["Nome", "Telefone", "Pele", "Anamnese", "Observacoes"]
        df = pd.DataFrame(columns=cols)
        df.to_csv(ARQUIVO_CLIENTES, index=False)
        return df
    return pd.read_csv(ARQUIVO_CLIENTES)

def cadastrar_cliente(dado_cliente):
    df = carregar_clientes()
    if dado_cliente["Nome"] in df["Nome"].values:
        return False, "Cliente já cadastrada com esse nome!"
    
    novo_df = pd.DataFrame([dado_cliente])
    df = pd.concat([df, novo_df], ignore_index=True)
    df.to_csv(ARQUIVO_CLIENTES, index=False)
    return True, "Cliente cadastrada com sucesso!"