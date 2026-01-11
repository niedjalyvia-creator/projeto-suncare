def analisar_sessao(pele, servico, hora_agendamento_str):
    """
    Define a sugestão de tempo POR POSIÇÃO baseada no horário (Sol forte x Sol fraco).
    """
    
    # 1. Lógica para MÁQUINA (CABINE) - Fixa
    if servico == "Máquina (Cabine)":
        return {
            "tempo_posicao": 15,
            "msg_seguranca": "Fazer 15 min Frente + 15 min Costas (+ Tempo de Corte)",
            "risco": "Controlado (Máquina)"
        }

    # 2. Lógica para SOL NATURAL
    # Tenta ler a hora (ex: "09:30" vira 9)
    try:
        hora = int(hora_agendamento_str.split(':')[0])
    except:
        hora = 8 # Se der erro, assume 8h por segurança

    sol_forte = hora >= 8  # Regra: Passou das 8h, o sol queima mais
    
    # Configuração de Tempos (Minutos por Posição)
    if "Tipo I" in pele or "Tipo II" in pele:
        # Peles Sensíveis
        tempo = 10 if sol_forte else 15
        obs = "Sol Forte! Ciclos curtos (10 min)." if sol_forte else "Sol ameno (15 min/lado)."
        risco = "🔴 ALTO (Cuidado Extra)"
        
    elif "Tipo III" in pele:
        # Morena Clara
        tempo = 15 if sol_forte else 20
        obs = "Reduzir tempo por conta do horário." if sol_forte else "Horário tranquilo."
        risco = "🟡 MODERADO"
        
    else:
        # Morenas e Negras (Tipo IV, V, VI)
        tempo = 20 if sol_forte else 30
        obs = "Pele resistente, mas hidrate."
        risco = "🟢 BAIXO"

    return {
        "tempo_posicao": tempo,
        "msg_seguranca": f"Sugestão: Ciclos de {tempo} min ({obs})",
        "risco": risco
    }