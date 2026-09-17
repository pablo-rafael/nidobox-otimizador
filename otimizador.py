import pandas as pd
import pulp

def calcular_otimizacao(orcamento, teto_pct, dados_canais):
    # 1. Transformar dados recebidos em DataFrame
    df = pd.DataFrame(dados_canais)
    canais = df['canal'].tolist()
    
    # 2. Inicializar o problema de Maximização
    modelo = pulp.LpProblem("Otimizacao_Nidobox", pulp.LpMaximize)
    
    # 3. Variáveis de Decisão (Valor a investir em cada canal, min: 0)
    investimento = pulp.LpVariable.dicts("Verba", canais, lowBound=0, cat='Continuous')
    
    # 4. Função Objetivo (Maximizar Visualizações totais)
    modelo += pulp.lpSum([investimento[c] * float(df.loc[df['canal'] == c, 'views_por_real'].values[0]) for c in canais])
    
    # 5. Restrição A: Orçamento Total
    modelo += pulp.lpSum([investimento[c] for c in canais]) <= float(orcamento)
    
    # 6. Restrição B: Teto de Diversificação
    limite_por_canal = float(orcamento) * (float(teto_pct) / 100.0)
    for c in canais:
        modelo += investimento[c] <= limite_por_canal
        
    # 7. Resolver o modelo
    modelo.solve()
    
    # 8. Montar o dicionário de resposta
    resultado = []
    visualizacoes_totais = 0
    
    for c in canais:
        valor = investimento[c].varValue if investimento[c].varValue is not None else 0
        views = valor * float(df.loc[df['canal'] == c, 'views_por_real'].values[0])
        visualizacoes_totais += views
        
        resultado.append({
            "canal": c,
            "valor_alocado": round(valor, 2),
            "visualizacoes": round(views)
        })
        
    return {
        "status": pulp.LpStatus[modelo.status],
        "alocacao": resultado,
        "visualizacoes_projetadas_totais": round(visualizacoes_totais)
    }