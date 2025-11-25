
import streamlit as st

st.set_page_config(
    page_title="Análise de Potencial de Investigação",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Análise de Potencial de Investigação")

st.sidebar.success("Selecione uma página acima.")

st.markdown(
    """
    ### Bem-vindo à ferramenta de Análise de Potencial de Investigação.

    Esta aplicação funciona como uma ferramenta de apoio à decisão, projetada para auxiliar na avaliação do **potencial de investigação** de uma ocorrência recém-registrada. 
    
    Utilize uma das duas abordagens de análise:
    
    1. **Previsão com Modelo de Machine Learning**: Utiliza um modelo preditivo treinado 
       para estimar a viabilidade da investigação.
    2. **Previsão com Regras de Negócio**: Aplica um conjunto de regras pré-definidas 
       para classificar a ocorrência.

    **👈 Selecione uma das páginas no menu ao lado para começar.**
    
    ### Como usar:
    - Navegue até a página desejada (Modelo ou Regras).
    - Preencha os detalhes da ocorrência no formulário.
    - Clique em "Analisar" para obter a previsão.
"""
)
