
import streamlit as st
import requests
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(page_title="Previsão com Modelo", page_icon="🤖", layout="wide")

st.title("🤖 Previsão de Potencial de Investigação (Modelo ML)")

# --- Formulário de Entrada ---
with st.form("ocorrencia_form_modelo", width=770):
    st.subheader("Detalhes da Ocorrência")
    
    periodo_decorrido_dias = st.number_input(
        "Período Decorrido (dias)", 
        min_value=0, 
        help="Há quantos dias a ocorrência foi registrada."
    )
    
    st.markdown("---") # Adiciona uma linha separadora visual

    # Duas colunas para os campos de seleção
    col1, col2 = st.columns(2)
    
    with col1:
        suspeito_conhecido = st.checkbox(
            "Suspeito é conhecido?",
            help="Marque se a vítima ou testemunhas conhecem o suspeito."
        )
        tem_testemunhas = st.checkbox(
            "Há testemunhas?",
            help="Marque se existem testemunhas presenciais do fato."
        )
        tem_imagens_cameras = st.checkbox(
            "Existem imagens de câmeras?",
            help="Marque se há imagens de câmeras de segurança que registraram o fato."
        )

    with col2:
        suspeito_rastreavel = st.checkbox(
            "Suspeito é rastreável?",
            help="Marque se há informações que permitam rastrear o suspeito (placa de veículo, celular, etc.)."
        )
        vestigios_preservados = st.checkbox(
            "Vestígios foram preservados?",
            help="Marque se o local do crime e os vestígios foram devidamente preservados."
        )


    submit_button = st.form_submit_button(label="Analisar Potencial")

# --- Lógica de Previsão ---
if submit_button:
    # URL do endpoint da API do modelo
    API_URL = "http://127.0.0.1:8002/prever" 

    # Montar o payload da requisição
    ocorrencia_data = {
        "periodo_decorrido_dias": periodo_decorrido_dias,
        "suspeito_conhecido": suspeito_conhecido,
        "tem_testemunhas": tem_testemunhas,
        "tem_imagens_cameras": tem_imagens_cameras,
        "suspeito_rastreavel": suspeito_rastreavel,
        "vestigios_preservados": vestigios_preservados,
    }

    st.info("Analisando com o modelo de Machine Learning...")

    try:
        response = requests.post(API_URL, json=ocorrencia_data)
        response.raise_for_status()  # Lança erro para status HTTP 4xx/5xx

        resultado = response.json()

        # Exibir o resultado
        st.subheader("Resultado da Análise")
        
        resolutividade = resultado.get("resolutividade", "N/A").upper()
        motivo = resultado.get("motivo", "Sem detalhes.")

        if resolutividade == "ALTA":
            st.success(f"**Potencial de Investigação: {resolutividade}**")
        elif resolutividade == "MÉDIA":
            st.warning(f"**Potencial de Investigação: {resolutividade}**")
        else:
            st.error(f"**Potencial de Investigação: {resolutividade}**")
            
        st.info(f"**Justificativa:** {motivo}")

    except requests.exceptions.RequestException as e:
        st.error(f"**Erro ao conectar com a API:** {e}")
        st.warning(
            "Verifique se a API do **modelo** está em execução na porta 8002. "
            "Use o comando: `uvicorn src.api.main_modelo:app --reload --port 8002`"
        )
