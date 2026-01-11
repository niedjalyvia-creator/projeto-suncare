import streamlit as st
import pandas as pd
import time
import urllib.parse
from datetime import datetime
import plotly.express as px
import banco
import regras

# --- FUNÇÕES ÚTEIS ---
def limpar_telefone(telefone):
    if not telefone: return ""
    return "".join(filter(str.isdigit, str(telefone)))

def formatar_data_ao_digitar():
    valor = st.session_state.chave_data
    apenas_nums = "".join(filter(str.isdigit, valor))
    if len(apenas_nums) == 8:
        st.session_state.chave_data = f"{apenas_nums[:2]}/{apenas_nums[2:4]}/{apenas_nums[4:]}"

def formatar_hora_ao_digitar():
    valor = st.session_state.chave_hora
    apenas_nums = "".join(filter(str.isdigit, valor))
    if len(apenas_nums) == 4:
        st.session_state.chave_hora = f"{apenas_nums[:2]}:{apenas_nums[2:]}"
    elif len(apenas_nums) == 3:
        st.session_state.chave_hora = f"0{apenas_nums[:1]}:{apenas_nums[1:]}"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SunCare Elite", page_icon="☀️", layout="wide")

# Inicialização de Variáveis
if "chave_data" not in st.session_state: st.session_state.chave_data = datetime.now().strftime("%d/%m/%Y")
if "chave_hora" not in st.session_state: st.session_state.chave_hora = datetime.now().strftime("%H:%M")
if "cronometros_ativos" not in st.session_state: st.session_state.cronometros_ativos = {}

# --- CSS DE LUXO (A MÁGICA ACONTECE AQUI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');
    
    /* Fundo Geral da Página - Um tom Off-White quentinho */
    .stApp {
        background-color: #FDFBF7; 
        font-family: 'Montserrat', sans-serif;
    }
    
    /* SIDEBAR - Um tom areia mais escuro para contraste */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9F4E6 0%, #FFFFFF 100%);
        border-right: 2px solid #D4AF37;
    }
    
    /* TITULOS - Dourado Escuro */
    h1, h2, h3 {
        color: #8A6E2F !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* CARDS COLORIDOS (Caixas de Fundo) */
    .card-champagne {
        background-color: #FFF8E1; /* Amarelo Champanhe Suave */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #D4AF37;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .card-bronze {
        background-color: #FBE9E7; /* Rosado Bronze Suave */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #B87333;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    
    /* INPUTS - Bordas Douradas */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #C5A028 !important;
        color: #333 !important;
        border-radius: 5px;
    }
    
    /* BOTÕES - Degradê Dourado Luxo */
    div.stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #B8860B 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #B8860B 0%, #D4AF37 100%);
        transform: scale(1.02);
    }

    /* ESTILIZAR METRICS */
    [data-testid="stMetricValue"] {
        color: #B87333 !important; /* Cor Bronze nos números */
    }
    
    /* DIVISOR */
    hr {
        border-top: 2px solid #E6D5A8; /* Linha dourada clara */
    }
    .card-white {
        background-color: #FFFDF5; /* Creme muito suave, não é mais branco puro */
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #E6D5A8; /* Borda dourada mais visível */
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.15); /* Sombra levemente dourada */
        margin-bottom: 20px;
    }

    /* NOVO: Cabeçalhos de Seção dentro do formulário */
    .section-header {
        background-color: #FDFBF7; /* Fundo sutil */
        color: #B8860B; /* Dourado escuro */
        padding: 8px 15px;
        border-radius: 5px;
        border-left: 4px solid #D4AF37;
        font-weight: 600;
        margin-bottom: 15px;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
try: st.sidebar.image("image.png", width=160)
except: 
    st.sidebar.markdown("<h2 style='text-align:center; color:#D4AF37;'>SUNCARE</h2>", unsafe_allow_html=True)

st.sidebar.markdown("### PAINEL DE CONTROLE")
menu = st.sidebar.radio("", ["CLIENTES", "AGENDAMENTO", "MESA DE BRONZE", "FINANCEIRO"])
st.sidebar.markdown("---")
st.sidebar.info(" Sistema Elite Bronze\nv2.0 Gold Edition")

# --- ABA 1: CLIENTES ---
if menu == "CLIENTES":
    st.markdown("<div class='card-champagne'><h1> GESTÃO DE CLIENTES</h1></div>", unsafe_allow_html=True)
    
    tab_novo, tab_lista = st.tabs(["NOVO CADASTRO", "BASE DE DADOS"])
    
    with tab_novo:
        # Envolvendo o formulário num card branco para destacar do fundo areia
        with st.container():
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.write("###  Ficha de Anamnese")
            with st.form("form_cadastro_cliente"):
                col_dados, col_saude = st.columns(2)
                with col_dados:
                    st.markdown("**DADOS PESSOAIS**")
                    nome_cli = st.text_input("Nome Completo")
                    tel_cli = st.text_input("WhatsApp (DDD + Número)")
                    pele_cli = st.selectbox("Fototipo", ["Tipo I - Muito Branca", "Tipo II - Branca", "Tipo III - Morena Clara", "Tipo IV - Morena", "Tipo V - Mulata", "Tipo VI - Negra"])
                with col_saude:
                    st.markdown("**SAÚDE & CUIDADOS**")
                    c1, c2 = st.columns(2)
                    check_hiper = c1.checkbox("Hipertensão")
                    check_diab = c2.checkbox("Diabetes")
                    check_grav = c1.checkbox("Gestante")
                    check_rem = c2.checkbox("Medicamentos")
                    check_desm = c1.checkbox("Desmaios")
                    check_cir = c2.checkbox("Cirurgias")
                    obs_cli = st.text_area("Observações")

                st.write("")
                if st.form_submit_button("SALVAR CADASTRO"):
                    if nome_cli:
                        probs = [p for p, c in [("Hipertensão", check_hiper), ("Diabetes", check_diab), ("Gestante", check_grav), ("Medicamentos", check_rem), ("Desmaios", check_desm), ("Cirurgias", check_cir)] if c]
                        txt_anamnese = ", ".join(probs) if probs else "Clinicamente Saudável"
                        sucesso, mensagem = banco.cadastrar_cliente({"Nome": nome_cli, "Telefone": tel_cli, "Pele": pele_cli, "Anamnese": txt_anamnese, "Observacoes": obs_cli})
                        if sucesso: st.success(mensagem)
                        else: st.error(mensagem)
                    else: st.warning("Nome obrigatório.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_lista:
        df_clientes = banco.carregar_clientes()
        if not df_clientes.empty:
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            lista_nomes = sorted(df_clientes["Nome"].unique())
            cliente_selecionada = st.selectbox(" Buscar Dossiê da Cliente:", lista_nomes)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if cliente_selecionada:
                dados = df_clientes[df_clientes["Nome"] == cliente_selecionada].iloc[0]
                
                # CARD DE DESTAQUE DA CLIENTE (FUNDO COLORIDO)
                st.markdown(f"""
                <div class='card-champagne'>
                    <div style='display:flex; justify-content:space-between;'>
                        <div>
                            <h2 style='margin:0; color:#333 !important;'>{cliente_selecionada}</h2>
                            <p style='color:#666;'>{dados['Pele']} | {dados['Telefone']}</p>
                        </div>
                        <div style='text-align:right;'>
                            <b style='color:#D4AF37;'>STATUS DE SAÚDE</b><br>
                            {dados['Anamnese']}
                        </div>
                    </div>
                    <hr>
                    <p><b>Notas:</b> {dados['Observacoes']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas em Card Bronze
                df_agenda = banco.carregar()
                historico = df_agenda[df_agenda["Cliente"] == cliente_selecionada] if not df_agenda.empty else pd.DataFrame()
                
                st.markdown("<div class='card-bronze'>", unsafe_allow_html=True)
                col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
                col_kpi1.metric("SESSÕES", len(historico))
                if not historico.empty:
                    col_kpi2.metric("ÚLTIMA", historico["Data"].iloc[-1])
                    col_kpi3.metric("TOTAL INVESTIDO", f"R$ {historico['Valor'].sum():.2f}")
                else:
                    col_kpi2.metric("ÚLTIMA", "-")
                    col_kpi3.metric("TOTAL INVESTIDO", "R$ 0.00")
                st.markdown("</div>", unsafe_allow_html=True)

                if not historico.empty:
                    st.write(" **Histórico Detalhado:**")
                    st.dataframe(historico[['Data', 'Servico', 'Tempo_Minutos', 'Valor']], use_container_width=True, hide_index=True)

# --- ABA 2: AGENDAMENTO ---
elif menu == "AGENDAMENTO":
    st.markdown("<div class='card-champagne'><h1> AGENDAMENTO DE SESSÕES</h1></div>", unsafe_allow_html=True)
    
    c_form, c_agenda = st.columns([1, 2])
    
    with c_form:
        st.markdown("<div class='card-white'>", unsafe_allow_html=True)
        st.write("### Nova Sessão")
        tipo = st.radio("Cliente", ["Cadastrada", "Avulsa"], horizontal=True)
        
        nome, pele, saude_msg = "", "Tipo IV - Morena", ""
        
        if tipo == "Cadastrada":
            df_cli = banco.carregar_clientes()
            if not df_cli.empty:
                nome = st.selectbox("Selecione:", sorted(df_cli["Nome"].unique()))
                d = df_cli[df_cli["Nome"] == nome].iloc[0]
                pele = d["Pele"]
                tel = d["Telefone"]
                if d["Anamnese"] not in ["Saudável", "Clinicamente Saudável"]:
                    saude_msg = f"⚠️ {d['Anamnese']}"
            else: st.warning("Sem cadastros.")
        else:
            nome = st.text_input("Nome")
            pele = st.selectbox("Pele", ["Tipo I", "Tipo II", "Tipo III", "Tipo IV", "Tipo V", "Tipo VI"])
            tel = st.text_input("Tel")

        if saude_msg:
            st.markdown(f"<div style='background:#FFEBEE; color:#C62828; padding:10px; border-radius:5px;'>{saude_msg}</div>", unsafe_allow_html=True)

        st.markdown("---")
        c_d, c_h = st.columns(2)
        c_d.text_input("Data", key="chave_data", on_change=formatar_data_ao_digitar)
        hora = c_h.text_input("Hora", key="chave_hora", on_change=formatar_hora_ao_digitar)
        servico = st.selectbox("Método", ["Sol Natural", "Máquina (Cabine)"])
        
        analise = regras.analisar_sessao(pele, servico, hora)
        
        # Caixa colorida de aviso
        cor_aviso = "#E3F2FD" # Azul claro
        if "ALTO" in analise['risco']: cor_aviso = "#FFEBEE" # Vermelho claro
        
        st.markdown(f"""
        <div style='background-color:{cor_aviso}; padding:15px; border-radius:8px; border-left:4px solid #D4AF37; margin:10px 0;'>
            <b>SUGESTÃO DO SISTEMA:</b><br>{analise['msg_seguranca']}
        </div>
        """, unsafe_allow_html=True)
        
        valor = st.number_input("Valor (R$)", value=50.0)
        
        if st.button("AGENDAR AGORA"):
            if nome:
                banco.salvar({"Cliente": nome, "Data": st.session_state.chave_data, "Hora": st.session_state.chave_hora, "Pele": pele, "Servico": servico, "Tempo_Minutos": analise['tempo_posicao'], "Risco": analise['risco'], "Valor": valor, "Status": "Agendado"})
                st.success("Agendado com Sucesso!")
                if tel and len(limpar_telefone(tel)) >= 10:
                    st.markdown(f"[ Enviar WhatsApp](https://wa.me/55{limpar_telefone(tel)})")
        st.markdown("</div>", unsafe_allow_html=True) # Fim card white

    with c_agenda:
        st.markdown("<div class='card-white'>", unsafe_allow_html=True)
        st.write("###  Visão da Agenda")
        df_a = banco.carregar()
        if not df_a.empty:
            hoje = datetime.now().strftime("%d/%m/%Y")
            df_hoje = df_a[df_a["Data"] == hoje]
            
            st.info(f"Hoje: {len(df_hoje)} clientes agendadas.")
            if not df_hoje.empty:
                st.dataframe(df_hoje[['Hora', 'Cliente', 'Servico', 'Tempo_Minutos']], hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.caption("Próximos Dias")
            df_a['Dt'] = pd.to_datetime(df_a['Data'], format='%d/%m/%Y', errors='coerce')
            fut = df_a[df_a['Dt'] > datetime.now()].sort_values('Dt')
            if not fut.empty:
                st.dataframe(fut[['Data', 'Hora', 'Cliente']], hide_index=True, use_container_width=True)
        else: st.write("Agenda livre.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- ABA 3: MESA DE CONTROLE ---
elif menu == "MESA DE BRONZE":
    st.markdown("<div class='card-champagne'><h1>⏱ MESA DE CONTROLE (AO VIVO)</h1></div>", unsafe_allow_html=True)
    
    with st.expander("▶️ INICIAR / VIRAR CLIENTE", expanded=True):
        df_all = banco.carregar()
        
        # --- AQUI ESTÁ A MÁGICA DO FILTRO ---
        hoje = datetime.now().strftime("%d/%m/%Y") # Pega a data de hoje
        
        # Filtra o banco: Só quero ver quem tem data igual a HOJE
        if not df_all.empty:
            df_hoje = df_all[df_all["Data"] == hoje]
        else:
            df_hoje = pd.DataFrame()
        # ------------------------------------

        if not df_hoje.empty:
            l_cli = df_hoje["Cliente"].unique() # Cria a lista curta
            
            c1, c2, c3 = st.columns([3, 2, 2])
            
            # O título da caixa muda para mostrar que é a lista de HOJE
            sel = c1.selectbox(f"Clientes do dia ({hoje})", l_cli)
            
            # Pega as infos EXATAS do agendamento de hoje
            info = df_hoje[df_hoje["Cliente"] == sel].iloc[0]
            sugest = int(info["Tempo_Minutos"])
            
            tempo = c2.number_input("Tempo (min)", value=sugest)
            
            if c3.button("INICIAR CICLO"):
                # Verifica se já tem tempo acumulado (caso seja a 2ª ou 3ª virada)
                ant = st.session_state.cronometros_ativos.get(sel, {}).get("acumulado", 0)
                
                st.session_state.cronometros_ativos[sel] = {
                    "inicio": datetime.now(), 
                    "tempo_restante_seg": tempo*60,
                    "acumulado": ant, 
                    "sugestao_ciclo": sugest, 
                    "pele": info["Pele"],
                    "status": "rodando", 
                    "ultima_atualizacao": datetime.now()
                }
                st.rerun()
        else:
            st.warning(f"Nenhum agendamento encontrado para hoje ({hoje}). Agende alguém na aba 'Agenda' primeiro.")

    st.markdown("---")
    ativos = st.session_state.cronometros_ativos
    
    if not ativos:
        st.info("Ninguém no sol no momento.")
    
    # Grid de Cards Ativos (Cronômetros)
    for nome, dados in list(ativos.items()):
        if dados["status"] == "rodando":
            now = datetime.now()
            dt = (now - dados["ultima_atualizacao"]).total_seconds()
            if dt >= 1:
                dados["tempo_restante_seg"] -= dt
                dados["acumulado"] += (dt/60)
                dados["ultima_atualizacao"] = now
        
        vis = max(0, dados["tempo_restante_seg"])
        m, s = int(vis//60), int(vis%60)
        
        # CARD DO CRONÔMETRO
        st.markdown(f"""
        <div class='card-bronze' style='margin-bottom:15px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <h3 style='margin:0; color:#B87333 !important;'>☀️ {nome}</h3>
                <span style='background:rgba(255,255,255,0.5); padding:5px 10px; border-radius:10px;'>{dados['pele']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            c_disp, c_act = st.columns([1, 2])
            with c_disp:
                if vis > 0: st.metric("⏳ Tempo Restante", f"{m:02d}:{s:02d}")
                else: st.error("🔔 TERMINOU - VIRAR")
                st.caption(f"Total Sol: {int(dados['acumulado'])} min")
            
            with c_act:
                st.write("⏱️ Ajustes Rápidos:")
                b_m5, b_m1, b_p1, b_p5 = st.columns(4)
                if b_m5.button("-5", key=f"m5_{nome}"): dados["tempo_restante_seg"] -= 300; st.rerun()
                if b_m1.button("-1", key=f"m1_{nome}"): dados["tempo_restante_seg"] -= 60; st.rerun()
                if b_p1.button("+1", key=f"p1_{nome}"): dados["tempo_restante_seg"] += 60; st.rerun()
                if b_p5.button("+5", key=f"p5_{nome}"): dados["tempo_restante_seg"] += 300; st.rerun()
                
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                
                a1, a2 = st.columns(2)
                if dados["status"] == "rodando":
                    if a1.button("⏸️ PAUSAR", key=f"ps_{nome}"): dados["status"] = "pausado"; st.rerun()
                else:
                    if a1.button("▶️ RETOMAR", key=f"pl_{nome}"): dados["status"] = "rodando"; dados["ultima_atualizacao"] = datetime.now(); st.rerun()
                
                if a2.button("✅ FINALIZAR", key=f"fn_{nome}"):
                    del st.session_state.cronometros_ativos[nome]
                    st.rerun()
    
    if ativos: time.sleep(1); st.rerun()

    st.markdown("---")
    ativos = st.session_state.cronometros_ativos
    
    if not ativos:
        st.info("Ninguém no sol no momento.")
    
    # Grid de Cards Ativos
    for nome, dados in list(ativos.items()):
        if dados["status"] == "rodando":
            now = datetime.now()
            dt = (now - dados["ultima_atualizacao"]).total_seconds()
            if dt >= 1:
                dados["tempo_restante_seg"] -= dt
                dados["acumulado"] += (dt/60)
                dados["ultima_atualizacao"] = now
        
        vis = max(0, dados["tempo_restante_seg"])
        m, s = int(vis//60), int(vis%60)
        
        # CARD DO CRONÔMETRO (BRONZE SUAVE)
        st.markdown(f"""
        <div class='card-bronze' style='margin-bottom:15px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <h3 style='margin:0; color:#B87333 !important;'>☀️ {nome}</h3>
                <span style='background:rgba(255,255,255,0.5); padding:5px 10px; border-radius:10px;'>{dados['pele']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Controles dentro de um container branco
        with st.container():
            c_disp, c_act = st.columns([1, 2])
            with c_disp:
                if vis > 0: st.metric("⏳ Tempo Restante", f"{m:02d}:{s:02d}")
                else: st.error("🔔 TERMINOU - VIRAR")
                st.caption(f"Total Sol: {int(dados['acumulado'])} min")
            
            with c_act:
                st.write("⏱️ Ajustar Tempo:")
                # Agora são 4 colunas para caber todos os botões
                b_menos5, b_menos1, b_mais1, b_mais5 = st.columns(4)
                
                # Botão -5 min
                if b_menos5.button("-5", key=f"m5_{nome}"): 
                    dados["tempo_restante_seg"] -= 300 
                    st.rerun()
                
                # Botão -1 min
                if b_menos1.button("-1", key=f"m1_{nome}"): 
                    dados["tempo_restante_seg"] -= 60
                    st.rerun()
                
                # Botão +1 min
                if b_mais1.button("+1", key=f"p1_{nome}"): 
                    dados["tempo_restante_seg"] += 60
                    st.rerun()
                
                # Botão +5 min
                if b_mais5.button("+5", key=f"p5_{nome}"): 
                    dados["tempo_restante_seg"] += 300
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True) # Espacinho
                
                # Botões de Ação (Pausar/Finalizar)
                a1, a2 = st.columns(2)
                if dados["status"] == "rodando":
                    if a1.button("⏸️ PAUSAR", key=f"ps_{nome}"): 
                        dados["status"] = "pausado"
                        st.rerun()
                else:
                    if a1.button("▶️ RETOMAR", key=f"pl_{nome}"): 
                        dados["status"] = "rodando"
                        dados["ultima_atualizacao"] = datetime.now()
                        st.rerun()
                
                if a2.button("✅ FINALIZAR", key=f"fn_{nome}"):
                    del st.session_state.cronometros_ativos[nome]
                    st.rerun()
    
    if ativos: time.sleep(1); st.rerun()

# --- ABA 4: FINANCEIRO ---
elif menu == "FINANCEIRO":
    st.markdown("<div class='card-champagne'><h1> DASHBOARD FINANCEIRO</h1></div>", unsafe_allow_html=True)
    
    df = banco.carregar()
    if not df.empty and "Valor" not in df.columns: df["Valor"] = 0.0
    
    if not df.empty:
        # Cards de KPI com fundo colorido
        st.markdown("<div class='card-bronze'>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.metric("FATURAMENTO TOTAL", f"R$ {df['Valor'].sum():.2f}")
        k2.metric("SESSÕES", len(df))
        media = df['Valor'].mean() if len(df) > 0 else 0
        k3.metric("TICKET MÉDIO", f"R$ {media:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_g, col_t = st.columns([1, 2])
        with col_g:
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.write("<b>Receita por Serviço</b>", unsafe_allow_html=True)
            fig = px.pie(df, names='Servico', values='Valor', color_discrete_sequence=['#D4AF37', '#B87333', '#8A6E2F'])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_t:
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.write("<b>Extrato Recente</b>", unsafe_allow_html=True)
            st.dataframe(df[['Data', 'Cliente', 'Servico', 'Valor']], use_container_width=True, height=250)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Sem dados financeiros.")