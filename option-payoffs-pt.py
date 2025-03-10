import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import exp

st.set_page_config(page_title="Explorador de Opções e Derivativos", layout="wide")

st.title("Explorador de Opções e Derivativos")
st.markdown("""
Esta aplicação ajuda-o a compreender os conceitos-chave de opções e derivativos através de visualizações interativas.
Explore os payoffs de opções, estratégias e fatores que afetam os preços.

*Criado por Luís Simões da Cunha*
""")

# Adicionar informações de licença e aviso legal
with st.expander("Licença e Aviso Legal"):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png", width=120)
    with col2:
        st.markdown("""
        ### Licença CC BY-NC
        Este trabalho está licenciado sob uma [Licença Creative Commons Atribuição-NãoComercial 4.0 Internacional](https://creativecommons.org/licenses/by-nc/4.0/).
        
        ### Aviso Legal
        - Esta aplicação destina-se apenas a fins educacionais.
        - O autor não é um consultor financeiro licenciado, e este conteúdo não deve ser tomado como aconselhamento financeiro.
        - As informações fornecidas são simplificadas para fins educacionais e podem não refletir todas as complexidades do mercado.
        - A negociação de opções envolve risco significativo e potencial de perda.
        - A precisão dos modelos e cálculos não é garantida.
        - Os utilizadores devem consultar profissionais qualificados antes de tomar decisões de investimento.
        """)

# Barra lateral para navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para", ["Opções Básicas", "Estratégias de Opções", "Paridade Put-Call", "Fatores que Afetam o Preço"])

# Funções básicas para calcular payoffs
def call_payoff(S, K):
    return np.maximum(S - K, 0)

def put_payoff(S, K):
    return np.maximum(K - S, 0)

def binary_call_payoff(S, K):
    return (S > K).astype(int)

def binary_put_payoff(S, K):
    return (S < K).astype(int)

# Página de Opções Básicas
if page == "Opções Básicas":
    st.header("Tipos Básicos de Opções")
    
    st.markdown("""
    ### Conceitos-Chave
    
    - **Opção de Compra (Call)**: O direito de comprar um ativo a um preço de exercício acordado numa data específica
    - **Opção de Venda (Put)**: O direito de vender um ativo a um preço de exercício acordado numa data específica
    - **Preço de Exercício**: O preço ao qual a opção pode ser exercida
    - **Valor Intrínseco**: O payoff se exercido imediatamente
    - **Valor Temporal**: Qualquer valor acima do valor intrínseco devido ao potencial futuro
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros da Opção")
        S0 = st.slider("Preço Atual do Ativo (€)", 50, 150, 100)
        K = st.slider("Preço de Exercício (€)", 50, 150, 100)
        premium = st.slider("Prémio da Opção (€)", 0, 20, 5)
        
        # Gerar intervalo de preços
        S_range = np.linspace(50, 150, 100)
        
        option_type = st.radio("Tipo de Opção", ["Call", "Put", "Call Binária", "Put Binária"])
        
        if option_type == "Call":
            payoff = call_payoff(S_range, K)
            profit = call_payoff(S_range, K) - premium
            title = f"Opção de Compra (K={K}€)"
            formula = r"Payoff Call = max(S - K, 0)"
        elif option_type == "Put":
            payoff = put_payoff(S_range, K)
            profit = put_payoff(S_range, K) - premium
            title = f"Opção de Venda (K={K}€)"
            formula = r"Payoff Put = max(K - S, 0)"
        elif option_type == "Call Binária":
            payoff = binary_call_payoff(S_range, K)
            profit = binary_call_payoff(S_range, K) - premium
            title = f"Opção de Compra Binária (K={K}€)"
            formula = r"Payoff Call Binária = 1 se S > K, 0 caso contrário"
        else:  # Put Binária
            payoff = binary_put_payoff(S_range, K)
            profit = binary_put_payoff(S_range, K) - premium
            title = f"Opção de Venda Binária (K={K}€)"
            formula = r"Payoff Put Binária = 1 se S < K, 0 caso contrário"
    
    with col2:
        st.subheader("Diagrama de Payoff")
        st.markdown(f"**Fórmula**: {formula}")

        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Traçar linhas de payoff e lucro
        ax.plot(S_range, payoff, 'b-', linewidth=2, label='Payoff no Vencimento')
        ax.plot(S_range, profit, 'g--', linewidth=2, label='Lucro (após prémio)')
        
        # Adicionar o ponto de break-even
        if option_type == "Call":
            breakeven = K + premium
            if breakeven <= 150:
                ax.axvline(x=breakeven, color='r', linestyle=':', label=f'Break-even ({breakeven}€)')
        elif option_type == "Put":
            breakeven = K - premium
            if breakeven >= 50:
                ax.axvline(x=breakeven, color='r', linestyle=':', label=f'Break-even ({breakeven}€)')
        
        # Adicionar o preço de exercício
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        # Marcador de preço atual
        ax.axvline(x=S0, color='purple', linestyle='-', label=f'Preço Atual ({S0}€)')
        
        # Destacar linha zero
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        ax.set_title(title)
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff/Lucro (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Resumo de valor
        st.subheader("Resumo do Valor Atual")
        current_intrinsic = 0
        if option_type == "Call":
            current_intrinsic = max(S0 - K, 0)
        elif option_type == "Put":
            current_intrinsic = max(K - S0, 0)
        elif option_type == "Call Binária":
            current_intrinsic = 1 if S0 > K else 0
        else:  # Put Binária
            current_intrinsic = 1 if S0 < K else 0
            
        time_value = max(0, premium - current_intrinsic)
        
        value_data = {
            "Componente": ["Valor Intrínseco", "Valor Temporal", "Prémio Total"],
            "Valor (€)": [current_intrinsic, time_value, premium]
        }
        
        st.table(pd.DataFrame(value_data))
        
        # Estado in-the-money/out-of-the-money
        status = ""
        if option_type in ["Call", "Call Binária"]:
            if S0 > K:
                status = "In-the-money"
            elif S0 < K:
                status = "Out-of-the-money"
            else:
                status = "At-the-money"
        else:  # Opções Put
            if S0 < K:
                status = "In-the-money"
            elif S0 > K:
                status = "Out-of-the-money"
            else:
                status = "At-the-money"
                
        st.markdown(f"**Estado**: {status}")
    
    st.markdown("""
    ### Compreender os Payoffs de Opções
    - A **linha azul** mostra o payoff da opção no vencimento
    - A **linha verde tracejada** mostra o lucro após contabilizar o prémio pago
    - O **ponto de break-even** é onde o lucro torna-se positivo
    """)

# Página de Estratégias de Opções
elif page == "Estratégias de Opções":
    st.header("Estratégias de Opções")
    
    st.markdown("""
    As estratégias de opções envolvem combinar opções com diferentes preços de exercício, vencimentos 
    ou tipos para criar perfis de payoff específicos para diferentes visões de mercado.
    """)
    
    strategy = st.selectbox("Selecionar Estratégia", [
        "Bull Spread", "Bear Spread", "Straddle", "Strangle", 
        "Butterfly Spread", "Risk Reversal"
    ])
    
    S_range = np.linspace(50, 150, 100)
    
    if strategy == "Bull Spread":
        st.subheader("Bull Spread")
        st.markdown("""
        Um **Bull Spread** é criado comprando uma opção de compra com um preço de exercício 
        mais baixo e vendendo uma opção de compra com um preço de exercício mais alto. Esta estratégia:
        - Beneficia de aumentos moderados de preço
        - Limita tanto o lucro potencial quanto a perda
        - Reduz o custo em comparação com apenas comprar uma opção de compra
        """)
        
        K1 = st.slider("Preço de Exercício Mais Baixo (€)", 70, 100, 90)
        K2 = st.slider("Preço de Exercício Mais Alto (€)", K1, 130, 110)
        
        long_call = call_payoff(S_range, K1)
        short_call = -call_payoff(S_range, K2)
        spread_payoff = long_call + short_call
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, long_call, 'b--', label=f'Call Longa (K={K1}€)')
        ax.plot(S_range, short_call, 'r--', label=f'Call Curta (K={K2}€)')
        ax.plot(S_range, spread_payoff, 'g-', linewidth=3, label='Payoff Bull Spread')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.set_title(f"Bull Spread (K1={K1}€, K2={K2}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: {K2-K1}€ (quando o preço do ativo ≥ {K2}€)  
        **Perda Máxima**: Custo do spread (prémio pago pela call K1 menos prémio recebido pela call K2)  
        **Break-even**: Preço de exercício mais baixo + prémio líquido pago
        
        **Fórmula**: Payoff Bull Spread = max(S-K1, 0) - max(S-K2, 0)
        """)
    
    elif strategy == "Bear Spread":
        st.subheader("Bear Spread")
        st.markdown("""
        Um **Bear Spread** é criado comprando uma opção de venda com um preço de exercício mais alto 
        e vendendo uma opção de venda com um preço de exercício mais baixo. Esta estratégia:
        - Beneficia de diminuições moderadas de preço
        - Limita tanto o lucro potencial quanto a perda
        - Reduz o custo em comparação com apenas comprar uma opção de venda
        """)
        
        K1 = st.slider("Preço de Exercício Mais Baixo (€)", 70, 100, 90)
        K2 = st.slider("Preço de Exercício Mais Alto (€)", K1, 130, 110)
        
        long_put = put_payoff(S_range, K2)
        short_put = -put_payoff(S_range, K1)
        spread_payoff = long_put + short_put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, long_put, 'b--', label=f'Put Longa (K={K2}€)')
        ax.plot(S_range, short_put, 'r--', label=f'Put Curta (K={K1}€)')
        ax.plot(S_range, spread_payoff, 'g-', linewidth=3, label='Payoff Bear Spread')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.set_title(f"Bear Spread (K1={K1}€, K2={K2}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: {K2-K1}€ (quando o preço do ativo ≤ {K1}€)  
        **Perda Máxima**: Custo do spread (prémio pago pela put K2 menos prémio recebido pela put K1)  
        **Break-even**: Preço de exercício mais alto - prémio líquido pago
        
        **Fórmula**: Payoff Bear Spread = max(K2-S, 0) - max(K1-S, 0)
        """)
    
    elif strategy == "Straddle":
        st.subheader("Straddle")
        st.markdown("""
        Um **Straddle** envolve comprar tanto uma opção de compra quanto uma opção de venda com o mesmo preço 
        de exercício e data de vencimento. Esta estratégia:
        - Beneficia de grandes movimentos de preço em qualquer direção
        - Utilizada quando se espera volatilidade significativa ou um anúncio importante
        - Lucrativa se o preço se mover mais do que os prémios combinados
        """)
        
        K = st.slider("Preço de Exercício (€)", 70, 130, 100)
        
        call = call_payoff(S_range, K)
        put = put_payoff(S_range, K)
        straddle_payoff = call + put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call, 'b--', label=f'Call (K={K}€)')
        ax.plot(S_range, put, 'r--', label=f'Put (K={K}€)')
        ax.plot(S_range, straddle_payoff, 'g-', linewidth=3, label='Payoff Straddle')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício (K={K}€)')
        
        ax.set_title(f"Straddle (K={K}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: Ilimitado (aumenta à medida que o preço se afasta do exercício)  
        **Perda Máxima**: Prémio combinado da call e da put (ocorre se o preço = exercício no vencimento)  
        **Pontos de Break-even**: Exercício + prémio combinado OU Exercício - prémio combinado
        
        **Fórmula**: Payoff Straddle = max(S-K, 0) + max(K-S, 0) = |S-K|
        """)
    
    elif strategy == "Strangle":
        st.subheader("Strangle")
        st.markdown("""
        Um **Strangle** envolve comprar uma call out-of-the-money e uma put out-of-the-money. Esta estratégia:
        - Beneficia de grandes movimentos de preço em qualquer direção
        - Mais barata que um straddle, mas requer movimento de preço maior para ser lucrativa
        - Utilizada quando se espera volatilidade significativa mas com maior tolerância ao risco
        """)
        
        K1 = st.slider("Preço de Exercício da Put (€)", 70, 100, 90)
        K2 = st.slider("Preço de Exercício da Call (€)", K1, 130, 110)
        
        call = call_payoff(S_range, K2)
        put = put_payoff(S_range, K1)
        strangle_payoff = call + put
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call, 'b--', label=f'Call (K={K2}€)')
        ax.plot(S_range, put, 'r--', label=f'Put (K={K1}€)')
        ax.plot(S_range, strangle_payoff, 'g-', linewidth=3, label='Payoff Strangle')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle='--', label=f'Exercício Put ({K1}€)')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'Exercício Call ({K2}€)')
        
        ax.set_title(f"Strangle (K1={K1}€, K2={K2}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: Ilimitado (aumenta à medida que o preço se afasta dos exercícios)  
        **Perda Máxima**: Prémio combinado da call e da put (ocorre se o preço estiver entre os exercícios no vencimento)  
        **Pontos de Break-even**: Exercício inferior - prémio combinado OU Exercício superior + prémio combinado
        
        **Fórmula**: Payoff Strangle = max(S-K2, 0) + max(K1-S, 0)
        """)
    
    elif strategy == "Butterfly Spread":
        st.subheader("Butterfly Spread")
        st.markdown("""
        Um **Butterfly Spread** envolve comprar uma call com um exercício mais baixo, vender duas calls com um exercício médio,
        e comprar uma call com um exercício mais alto. Esta estratégia:
        - Beneficia quando o preço permanece próximo do exercício médio
        - Tem risco limitado e potencial de lucro limitado
        - Utilizada quando se espera baixa volatilidade ou um preço estável
        """)
        
        K1 = st.slider("Preço de Exercício Mais Baixo (€)", 70, 90, 80)
        K2 = st.slider("Preço de Exercício Médio (€)", K1+10, 110, 100)
        K3 = st.slider("Preço de Exercício Mais Alto (€)", K2+10, 130, 120)
        
        call1 = call_payoff(S_range, K1)
        call2 = -2 * call_payoff(S_range, K2)
        call3 = call_payoff(S_range, K3)
        butterfly_payoff = call1 + call2 + call3
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, call1, 'b--', label=f'Call Longa (K={K1}€)')
        ax.plot(S_range, call2, 'r--', label=f'2 Calls Curtas (K={K2}€)')
        ax.plot(S_range, call3, 'y--', label=f'Call Longa (K={K3}€)')
        ax.plot(S_range, butterfly_payoff, 'g-', linewidth=3, label='Payoff Butterfly')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle=':', label=f'K1={K1}€')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'K2={K2}€')
        ax.axvline(x=K3, color='gray', linestyle=':', label=f'K3={K3}€')
        
        ax.set_title(f"Butterfly Spread (K1={K1}€, K2={K2}€, K3={K3}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: {K2-K1}€ (ocorre se o preço = exercício médio no vencimento)  
        **Perda Máxima**: Prémio líquido pago (limitado)  
        **Pontos de Break-even**: Exercício inferior + prémio líquido OU Exercício superior - prémio líquido
        
        **Fórmula**: Payoff Butterfly = max(S-K1, 0) - 2*max(S-K2, 0) + max(S-K3, 0)
        """)
    
    elif strategy == "Risk Reversal":
        st.subheader("Risk Reversal")
        st.markdown("""
        Um **Risk Reversal** envolve vender uma put out-of-the-money e comprar uma call out-of-the-money.
        Esta estratégia:
        - Cria uma posição semelhante a deter o ativo subjacente
        - Beneficia de preços em alta e é prejudicada por preços em queda
        - Pode ser estruturada para ser de custo zero (prémios compensam-se mutuamente)
        """)
        
        K1 = st.slider("Preço de Exercício da Put (€)", 70, 95, 90)
        K2 = st.slider("Preço de Exercício da Call (€)", 105, 130, 110)
        
        short_put = -put_payoff(S_range, K1)
        long_call = call_payoff(S_range, K2)
        risk_reversal_payoff = short_put + long_call
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(S_range, short_put, 'r--', label=f'Put Curta (K={K1}€)')
        ax.plot(S_range, long_call, 'b--', label=f'Call Longa (K={K2}€)')
        ax.plot(S_range, risk_reversal_payoff, 'g-', linewidth=3, label='Payoff Risk Reversal')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K1, color='gray', linestyle='--', label=f'Exercício Put ({K1}€)')
        ax.axvline(x=K2, color='gray', linestyle='--', label=f'Exercício Call ({K2}€)')
        
        ax.set_title(f"Risk Reversal (K1={K1}€, K2={K2}€)")
        ax.set_xlabel('Preço do Ativo no Vencimento (€)')
        ax.set_ylabel('Payoff (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown(f"""
        **Lucro Máximo**: Ilimitado (aumenta à medida que o preço sobe acima do exercício da call)  
        **Perda Máxima**: Limitada mas potencialmente grande (aumenta à medida que o preço cai abaixo do exercício da put)  
        
        **Fórmula**: Payoff Risk Reversal = max(S-K2, 0) - max(K1-S, 0)
        """)

# Página de Paridade Put-Call
elif page == "Paridade Put-Call":
    st.header("Paridade Put-Call")
    
    st.markdown("""
    A Paridade Put-Call é uma relação fundamental que conecta os preços das opções europeias de venda, 
    opções de compra, o ativo subjacente e uma obrigação sem risco.
    
    ### A Fórmula
    
    $$ C - P = S - K e^{-r(T-t)} $$
    
    Onde:
    - $C$ é o preço da call
    - $P$ é o preço da put
    - $S$ é o preço do ativo subjacente
    - $K$ é o preço de exercício
    - $r$ é a taxa de juro sem risco
    - $T-t$ é o tempo até ao vencimento em anos
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros")
        S0 = st.slider("Preço Atual do Ativo (€)", 50, 150, 100)
        K = st.slider("Preço de Exercício (€)", 50, 150, 100)
        r = st.slider("Taxa Sem Risco (%)", 0.0, 10.0, 5.0) / 100
        T = st.slider("Tempo até ao Vencimento (anos)", 0.1, 2.0, 1.0, 0.1)
        
        # Calcular preços teóricos (usando modelo muito básico para ilustração)
        vol = 0.2  # Volatilidade assumida
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        from scipy.stats import norm
        call_price = S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        put_price = K * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
        
        st.markdown(f"""
        ### Preços Teóricos
        - Preço da Opção de Compra: **{call_price:.2f}€**
        - Preço da Opção de Venda: **{put_price:.2f}€**
        - Valor Presente do Exercício: **{K*np.exp(-r*T):.2f}€**
        """)
        
        # Verificar paridade put-call
        left_side = call_price - put_price
        right_side = S0 - K * np.exp(-r*T)
        
        st.markdown(f"""
        ### Verificação da Paridade Put-Call
        - Lado Esquerdo (C - P): **{left_side:.2f}€**
        - Lado Direito (S - Ke^(-rT)): **{right_side:.2f}€**
        - Diferença: **{left_side - right_side:.4f}€** (deve ser próximo de zero)
        """)
        
    with col2:
        st.subheader("Representação Visual")
        
        # Gerar intervalo de preços
        S_range = np.linspace(50, 150, 100)
        
        # Calcular payoffs no vencimento
        call_payoff_values = call_payoff(S_range, K)
        put_payoff_values = put_payoff(S_range, K)
        stock_minus_bond = S_range - K  # No vencimento, o valor da obrigação é apenas K
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(S_range, call_payoff_values, 'b-', label='Payoff Call')
        ax.plot(S_range, -put_payoff_values, 'r-', label='-Payoff Put')
        ax.plot(S_range, call_payoff_values - put_payoff_values, 'g-', linewidth=3, 
                label='Call - Put')
        ax.plot(S_range, stock_minus_bond, 'k--', label='Ativo - Exercício')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        ax.set_title("Paridade Put-Call no Vencimento")
        ax.set_xlabel('Preço do Ativo (€)')
        ax.set_ylabel('Valor (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        st.markdown("""
        A linha verde (Call - Put) sobrepõe-se perfeitamente à linha preta tracejada (Ativo - Exercício) no vencimento,
        demonstrando a paridade put-call.
        
        ### Oportunidade de Arbitragem
        Se a paridade put-call não se mantiver no mercado, existe uma oportunidade de arbitragem:
        1. Se C - P > S - Ke^(-rT), venda a call, compre a put, venda o ativo a descoberto e invista Ke^(-rT)
        2. Se C - P < S - Ke^(-rT), compre a call, venda a put, compre o ativo e peça emprestado Ke^(-rT)
        """)

# Página de Fatores que Afetam o Preço
elif page == "Fatores que Afetam o Preço":
    st.header("Fatores que Afetam os Preços das Opções")
    
    st.markdown("""
    O preço de uma opção é influenciado por vários fatores-chave. Compreender estas relações
    é crucial para a negociação de opções e gestão de risco.
    """)
    
    factor = st.selectbox("Selecionar Fator para Explorar", [
        "Preço do Ativo Subjacente", "Tempo até ao Vencimento", "Volatilidade", 
        "Taxa de Juro", "Preço de Exercício"
    ])
    
    if factor == "Preço do Ativo Subjacente":
        st.subheader("Efeito do Preço do Ativo Subjacente")
        st.markdown("""
        O preço do ativo subjacente é um dos fatores mais importantes que afetam os preços das opções:
        - **Opções de compra** aumentam de valor quando o preço do ativo subjacente aumenta
        - **Opções de venda** diminuem de valor quando o preço do ativo subjacente aumenta
        
        Próximo do preço de exercício, os valores das opções são mais sensíveis às alterações no ativo subjacente.
        """)
        
        # Parâmetros
        K = 100
        r = 0.05
        T = 1.0
        vol = 0.2
        
        # Gerar intervalo de preços
        S_range = np.linspace(70, 130, 100)
        
        # Calcular preços teóricos usando aproximação Black-Scholes
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        from scipy.stats import norm
        call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
        put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(S_range, call_prices, 'b-', linewidth=2, label='Opção de Compra')
        ax.plot(S_range, put_prices, 'r-', linewidth=2, label='Opção de Venda')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        ax.set_title(f"Preços das Opções vs. Preço do Ativo Subjacente (Exercício={K}€)")
        ax.set_xlabel('Preço do Ativo Subjacente (€)')
        ax.set_ylabel('Preço da Opção (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Adicionar curva delta
        st.subheader("Delta: Taxa de Variação com o Preço do Ativo")
        
        # Calcular delta
        call_delta = norm.cdf(d1)
        put_delta = call_delta - 1
        
        # Gráfico delta
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(S_range, call_delta, 'b-', linewidth=2, label='Delta Call')
        ax2.plot(S_range, put_delta, 'r-', linewidth=2, label='Delta Put')
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        ax2.set_title(f"Delta da Opção vs. Preço do Ativo Subjacente (Exercício={K}€)")
        ax2.set_xlabel('Preço do Ativo Subjacente (€)')
        ax2.set_ylabel('Delta')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        **Delta** mede a taxa de variação do preço da opção em relação às variações no preço do ativo subjacente:
        - O delta da call varia de 0 a 1
        - O delta da put varia de -1 a 0
        - As opções at-the-money têm deltas de aproximadamente 0,5 (calls) ou -0,5 (puts)
        
        O delta é importante para a cobertura de risco e para entender a exposição da opção aos movimentos de preço.
        """)
        
    elif factor == "Tempo até ao Vencimento":
        st.subheader("Efeito do Tempo até ao Vencimento")
        st.markdown("""
        O tempo até ao vencimento afeta os preços das opções através do valor temporal:
        
        - As opções perdem valor à medida que se aproximam do vencimento (decaimento temporal)
        - A taxa de decaimento temporal (theta) acelera à medida que o vencimento se aproxima
        - As opções at-the-money são as mais afetadas pelo decaimento temporal
        - O valor temporal é maior para opções at-the-money
        """)
        
        # Parâmetros
        S0 = 100
        K = 100
        r = 0.05
        vol = 0.2
        
        # Intervalos de tempo
        T_values = [2.0, 1.0, 0.5, 0.25, 0.1, 0.01]
        
        # Intervalo de preços
        S_range = np.linspace(70, 130, 100)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for T in T_values:
            # Calcular preços das calls
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            ax.plot(S_range, call_prices, linewidth=2, label=f'T = {T} anos')
        
        # Adicionar a função de payoff
        payoff = np.maximum(S_range - K, 0)
        ax.plot(S_range, payoff, 'k--', linewidth=1, label='Payoff no vencimento')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        ax.set_title(f"Preços da Opção de Compra vs. Tempo até ao Vencimento (Exercício={K}€)")
        ax.set_xlabel('Preço do Ativo Subjacente (€)')
        ax.set_ylabel('Preço da Opção de Compra (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Ilustração do decaimento temporal
        st.subheader("Ilustração do Decaimento Temporal")
        
        # Preço fixo
        atm_call_prices = []
        otm_call_prices = []
        itm_call_prices = []
        days = np.linspace(365, 0, 100)
        years = days/365
        
        for T in years:
            if T == 0:
                # No vencimento
                atm_call = max(S0 - K, 0)
                otm_call = max(S0*0.9 - K, 0)
                itm_call = max(S0*1.1 - K, 0)
            else:
                # Calcular preços das calls
                # At-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                atm_call = S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
                
                # Out-of-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0*0.9/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                otm_call = S0*0.9 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
                
                # In-the-money
                d1 = 1/(vol*np.sqrt(T)) * (np.log(S0*1.1/K) + (r + vol**2/2)*T)
                d2 = d1 - vol*np.sqrt(T)
                itm_call = S0*1.1 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            atm_call_prices.append(atm_call)
            otm_call_prices.append(otm_call)
            itm_call_prices.append(itm_call)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(days, atm_call_prices, 'b-', linewidth=2, label='Call At-the-money')
        ax2.plot(days, otm_call_prices, 'r-', linewidth=2, label='Call Out-of-the-money')
        ax2.plot(days, itm_call_prices, 'g-', linewidth=2, label='Call In-the-money')
        
        ax2.set_title("Preço da Opção vs. Dias até ao Vencimento")
        ax2.set_xlabel('Dias até ao Vencimento')
        ax2.set_ylabel('Preço da Opção de Compra (€)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        O gráfico mostra como os preços das opções convergem para o seu valor intrínseco à medida que o vencimento se aproxima:
        
        - As **opções at-the-money** (linha azul) perdem todo o valor temporal no vencimento
        - As **opções out-of-the-money** (linha vermelha) tornam-se sem valor no vencimento se permanecerem out-of-the-money
        - As **opções in-the-money** (linha verde) mantêm o seu valor intrínseco, mas perdem o valor temporal
        
        Este decaimento temporal é conhecido como **theta** nos Gregos.
        """)
        
    elif factor == "Volatilidade":
        st.subheader("Efeito da Volatilidade")
        st.markdown("""
        A volatilidade mede a magnitude esperada dos movimentos de preço do ativo subjacente:
        
        - Maior volatilidade aumenta os preços das opções (tanto calls como puts)
        - A volatilidade é o único fator no preço das opções que não é diretamente observável
        - A volatilidade implícita é derivada dos preços de mercado das opções
        - A volatilidade tende a aumentar durante períodos de tensão no mercado
        """)
        
        # Parâmetros
        S0 = 100
        K = 100
        r = 0.05
        T = 1.0
        
        # Valores de volatilidade
        vol_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        # Intervalo de preços
        S_range = np.linspace(70, 130, 100)
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for vol in vol_values:
            # Calcular preços das calls
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            
            ax.plot(S_range, call_prices, linewidth=2, label=f'σ = {vol*100:.0f}%')
        
        # Adicionar a função de payoff
        payoff = np.maximum(S_range - K, 0)
        ax.plot(S_range, payoff, 'k--', linewidth=1, label='Payoff no vencimento')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=K, color='gray', linestyle='--', label=f'Exercício ({K}€)')
        
        ax.set_title(f"Preços da Opção de Compra vs. Volatilidade (Exercício={K}€)")
        ax.set_xlabel('Preço do Ativo Subjacente (€)')
        ax.set_ylabel('Preço da Opção de Compra (€)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
        
        # Ilustração do sorriso de volatilidade
        st.subheader("Sorriso de Volatilidade")
        
        # Criar dados sintéticos de volatilidade implícita para visualização
        strikes = np.linspace(80, 120, 9)
        atm_vol = 0.2
        
        # Sorriso de volatilidade sintético
        def vol_smile(k):
            return atm_vol + 0.001 * (k-K)**2
        
        implied_vols = [vol_smile(k) for k in strikes]
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(strikes, implied_vols, 'b-o', linewidth=2)
        
        ax2.axvline(x=S0, color='gray', linestyle='--', label=f'Preço Atual ({S0}€)')
        
        ax2.set_title("Sorriso de Volatilidade Implícita")
        ax2.set_xlabel('Preço de Exercício (€)')
        ax2.set_ylabel('Volatilidade Implícita')
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig2)
        
        st.markdown("""
        ### Sorriso de Volatilidade
        
        Na prática, a volatilidade implícita varia entre diferentes preços de exercício, criando um padrão de "sorriso":
        
        - Exercícios mais baixos (puts OTM/calls ITM) geralmente têm volatilidade implícita mais alta
        - Exercícios mais altos (puts ITM/calls OTM) geralmente têm volatilidade implícita mais alta
        - Este padrão contradiz a suposição de volatilidade constante no modelo Black-Scholes
        - O sorriso de volatilidade reflete preocupações do mercado sobre movimentos extremos de preço
        
        O vega (sensibilidade à volatilidade) é mais alto para opções at-the-money.
        """)
        
    elif factor == "Taxa de Juro":
        st.subheader("Efeito da Taxa de Juro")
        st.markdown("""
        As taxas de juro afetam os preços das opções de várias formas:
        
        - Taxas de juro mais altas geralmente aumentam os preços das opções de compra
        - Taxas de juro mais altas geralmente diminuem os preços das opções de venda
        - O efeito é geralmente menos significativo do que outros fatores
        - As taxas de juro afetam o valor presente do preço de exercício
        - O efeito relaciona-se com o valor temporal do dinheiro e o custo de manter o ativo subjacente
        """)
        
        # Parâmetros
        S0 = 100
        K = 100
        T = 1.0
        vol = 0.2
        
        # Valores de taxa de juro
        r_values = [0.01, 0.03, 0.05, 0.07, 0.10]
        
        # Intervalo de preços
        S_range = np.linspace(70, 130, 100)
        
        # Gráfico para opções de compra
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        for r in r_values:
            # Calcular preços das calls
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
            
            ax1.plot(S_range, call_prices, linewidth=2, label=f'r = {r*100:.0f}%')
            ax2.plot(S_range, put_prices, linewidth=2, label=f'r = {r*100:.0f}%')
        
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=K, color='gray', linestyle='--')
        ax1.set_title("Preços da Opção de Compra vs. Taxa de Juro")
        ax1.set_xlabel('Preço do Ativo Subjacente (€)')
        ax1.set_ylabel('Preço da Opção de Compra (€)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=K, color='gray', linestyle='--')
        ax2.set_title("Preços da Opção de Venda vs. Taxa de Juro")
        ax2.set_xlabel('Preço do Ativo Subjacente (€)')
        ax2.set_ylabel('Preço da Opção de Venda (€)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig)
        
        # Ilustração do valor presente
        st.subheader("Valor Presente do Preço de Exercício")
        
        r_range = np.linspace(0.01, 0.10, 100)
        pv_strike = [K * np.exp(-r*T) for r in r_range]
        
        fig2, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.plot(r_range*100, pv_strike, 'b-', linewidth=2)
        
        ax3.set_title(f"Valor Presente do Exercício (K={K}€, T={T} ano)")
        ax3.set_xlabel('Taxa de Juro (%)')
        ax3.set_ylabel('Valor Presente do Exercício (€)')
        ax3.grid(True, alpha=0.3)
        
        st.pyplot(fig2)
        
        st.markdown("""
        O valor presente do preço de exercício diminui à medida que as taxas de juro aumentam. Isto explica por que:
        
        - As opções de compra tornam-se mais valiosas com taxas mais altas (menor valor presente do exercício)
        - As opções de venda tornam-se menos valiosas com taxas mais altas (menor valor presente do exercício)
        
        Na paridade put-call: C - P = S - Ke^(-rT)
        """)
        
    elif factor == "Preço de Exercício":
        st.subheader("Efeito do Preço de Exercício")
        st.markdown("""
        O preço de exercício é um parâmetro fundamental nas opções:
        
        - As opções de compra diminuem de valor à medida que o preço de exercício aumenta
        - As opções de venda aumentam de valor à medida que o preço de exercício aumenta
        - As opções at-the-money (exercício ≈ preço atual) têm o maior valor temporal
        - As opções deep in-the-money comportam-se de forma semelhante ao ativo subjacente
        - As opções deep out-of-the-money têm delta baixo e são mais sensíveis à volatilidade
        """)
        
        # Parâmetros
        S0 = 100
        r = 0.05
        T = 1.0
        vol = 0.2
        
        # Valores de exercício
        K_values = [80, 90, 100, 110, 120]
        
        # Intervalo de preços
        S_range = np.linspace(70, 130, 100)
        
        # Gráfico
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        for K in K_values:
            # Calcular preços
            d1 = 1/(vol*np.sqrt(T)) * (np.log(S_range/K) + (r + vol**2/2)*T)
            d2 = d1 - vol*np.sqrt(T)
            call_prices = S_range * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            put_prices = K * np.exp(-r*T) * norm.cdf(-d2) - S_range * norm.cdf(-d1)
            
            ax1.plot(S_range, call_prices, linewidth=2, label=f'K = {K}€')
            ax2.plot(S_range, put_prices, linewidth=2, label=f'K = {K}€')
        
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=S0, color='gray', linestyle='--', label=f'Preço Atual ({S0}€)')
        ax1.set_title("Preços da Opção de Compra vs. Preço de Exercício")
        ax1.set_xlabel('Preço do Ativo Subjacente (€)')
        ax1.set_ylabel('Preço da Opção de Compra (€)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.axvline(x=S0, color='gray', linestyle='--', label=f'Preço Atual ({S0}€)')
        ax2.set_title("Preços da Opção de Venda vs. Preço de Exercício")
        ax2.set_xlabel('Preço do Ativo Subjacente (€)')
        ax2.set_ylabel('Preço da Opção de Venda (€)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        st.pyplot(fig)
        
        # Gráfico do preço da opção vs. exercício
        K_range = np.linspace(70, 130, 100)
        
        # Calcular preços
        d1 = 1/(vol*np.sqrt(T)) * (np.log(S0/K_range) + (r + vol**2/2)*T)
        d2 = d1 - vol*np.sqrt(T)
        call_prices = S0 * norm.cdf(d1) - K_range * np.exp(-r*T) * norm.cdf(d2)
        put_prices = K_range * np.exp(-r*T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
        
        fig2, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.plot(K_range, call_prices, 'b-', linewidth=2, label='Opção de Compra')
        ax3.plot(K_range, put_prices, 'r-', linewidth=2, label='Opção de Venda')
        
        ax3.axvline(x=S0, color='gray', linestyle='--', label=f'Preço Atual ({S0}€)')
        
        ax3.set_title(f"Preços das Opções vs. Preço de Exercício (S={S0}€)")
        ax3.set_xlabel('Preço de Exercício (€)')
        ax3.set_ylabel('Preço da Opção (€)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        st.pyplot(fig2)
        
        st.markdown("""
        Os gráficos mostram como os preços das opções variam com o preço de exercício:
        
        - Para calls: quanto menor o exercício, maior o valor
        - Para puts: quanto maior o exercício, maior o valor
        - As opções at-the-money (S ≈ K) têm o maior valor temporal e maior vega
        
        A seleção do preço de exercício é crítica nas estratégias de opções.
        """)

# Rodapé
st.markdown("---")
st.markdown("""
### Resumo
Esta aplicação demonstra os conceitos fundamentais da negociação de opções:

1. As opções dão direitos sem obrigações
2. Os principais fatores que afetam os preços das opções são:
   - Preço do ativo subjacente
   - Tempo até ao vencimento
   - Volatilidade
   - Taxas de juro
   - Preço de exercício

3. As estratégias de opções podem ser construídas para diferentes visões de mercado:
   - Visões direcionais (bull/bear spreads)
   - Visões de volatilidade (straddles/strangles)
   - Visões de intervalo limitado (butterflies/condors)

4. A paridade put-call fornece uma relação fundamental entre os preços de calls e puts

### Sobre o Autor
Luís Simões da Cunha NÃO é um Consultor Financeiro, nem está habilitado a dar qualquer conselho sobre investimentos. O autor não possui quaisquer credenciais ou certificações na área financeira que o autorizem a prestar aconselhamento financeiro.

### Aviso Legal Adicional
Esta aplicação destina-se EXCLUSIVAMENTE a fins educativos. O material apresentado serve apenas como uma introdução simplificada aos conceitos de opções e derivativos, e NÃO como base para decisões de investimento.

A utilização desta ferramenta é feita por sua conta e risco. O autor não assume qualquer responsabilidade por:
- Perdas financeiras resultantes da aplicação dos conceitos aqui apresentados
- Imprecisões ou erros nos cálculos, fórmulas ou gráficos
- Desatualização da informação face a práticas de mercado atuais
- Omissão de fatores relevantes que afetam o preço real das opções

Os modelos utilizados são simplificações e não capturam todas as complexidades dos mercados reais. A fiabilidade, precisão e exatidão dos resultados não são garantidas.

Antes de negociar opções ou qualquer instrumento financeiro, consulte um profissional financeiro devidamente credenciado.

### Contacto
Para questões apenas relacionadas com os aspetos educacionais da aplicação, por favor contacte o autor.

---
*© 2025 Luís Simões da Cunha. Todos os direitos reservados, exceto os concedidos sob a licença CC BY-NC.*
""")