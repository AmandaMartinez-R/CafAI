import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Função do agente
def agente_ia(novo_dado, modelo, meta_producao=40):
    previsao = modelo.predict(novo_dado)[0]
    sugestoes = []

    if novo_dado['pest_incidence'].values[0] > 0.3:
        sugestoes.append("Alta incidência de pragas! Reforce o controle fitossanitário.")
    
    if novo_dado['precip_mm'].values[0] < 900:
        sugestoes.append("Pouca chuva registrada. Considere irrigação para a cultura.")
    
    if previsao < meta_producao:
        sugestoes.append("Produtividade prevista abaixo da meta. Verifique manejo e condições gerais da lavoura.")
    
    return previsao, sugestoes

# --- Streamlit UI ---
st.title("CafAI: Seu Agente de IA para Previsão e Sugestões na Produção de Café ☕🌱")
st.markdown(
    """
    #### Como usar: 
    Preencha os dados abaixo para visualizar as previsões.  
    Os dados são baseados em modelos de IA treinados para monitorar pragas e otimizar a produção.  
    """
)

# Entradas do usuário para os dados do talhão
farm_id = st.number_input("ID da fazenda", min_value=1, step=1, value=1)
year = st.number_input("Ano da safra", min_value=2000, max_value=2100, value=2024)
altitude_m = st.number_input("Altitude (m)", value=1200)
avg_temp_C = st.number_input("Temperatura média (°C)", value=20.5)
precip_mm = st.number_input("Chuva acumulada (mm)", value=1100)
fertilizer_kg_ha = st.number_input("Fertilizante (kg/ha)", value=200)
irrigation = st.selectbox("Irrigação?", options=[0,1], index=1)
pruning_score = st.slider("Pontuação de poda (0 a 1)", min_value=0.0, max_value=1.0, value=0.8)
pest_incidence = st.slider("Incidência de pragas (0 a 1)", min_value=0.0, max_value=1.0, value=0.2)
prev_yield_sacas_ha = st.number_input("Produção anterior (sacas/ha)", value=35)

variety = st.selectbox("Variedade de café", options=["Catuai", "Icatu", "Mundo Novo"])

# Criar DataFrame com as dummies para as variedades
variety_dict = {"Catuai": [1,0,0], "Icatu": [0,1,0], "Mundo Novo": [0,0,1]}
variety_data = variety_dict[variety]

novo_dado = pd.DataFrame([{
    "farm_id": farm_id,
    "year": year,
    "altitude_m": altitude_m,
    "avg_temp_C": avg_temp_C,
    "precip_mm": precip_mm,
    "fertilizer_kg_ha": fertilizer_kg_ha,
    "irrigation": irrigation,
    "pruning_score": pruning_score,
    "pest_incidence": pest_incidence,
    "prev_yield_sacas_ha": prev_yield_sacas_ha,
    "variety_Catuai": variety_data[0],
    "variety_Icatu": variety_data[1],
    "variety_Mundo Novo": variety_data[2],
}])

# Carregar modelo previamente treinado e salvo 
#erro caso o arquivo não esteja salvo
try:
    with open("modelo_cafe.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Arquivo modelo_cafe.pkl não encontrado! Treine e salve seu modelo antes de rodar o app.")
    st.stop()

if st.button("Prever produtividade e receber sugestões"):
    prod, dicas = agente_ia(novo_dado, model)
    st.write(f"### Produtividade prevista: {prod:.2f} sacas/ha")
    if len(dicas) == 0:
        st.success("Nenhuma sugestão necessária, condições adequadas!")
    else:
        st.warning("Sugestões para o agricultor:")
        for dica in dicas:
            st.write(f"- {dica}")
