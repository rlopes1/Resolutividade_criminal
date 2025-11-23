from http.client import HTTPException
from fastapi import FastAPI
from src.models.schemas import OcorrenciaRequest, PrevisaoResponse
import joblib
import numpy as np


# --- Configuração da Aplicação ---
app = FastAPI(
    title="API de Análise de Resolutividade Criminal",
    description="Prevê o potencial de resolução de uma ocorrência com uso de Machine Learning.",
    version="1.0" 
)

# Classes de resolutividade
RESOLUTIVIDADE_CLASSES = {
    0: "Baixa",
    1: "Média",
    2: "Alta"
}


# Carregar modelo treinado
print("🤖 Carregando modelo ML...")
try:
     with open("src/api/resolutividade_model.pkl", "rb") as f:
        modelo = joblib.load(f)
        print("✓ Modelo carregado com sucesso!")
except FileNotFoundError:
    print("❌ Modelo não encontrado!")
    print("Execute primeiro: python gerar_modelo.py")
    modelo = None


# --- Endpoints da API ---

@app.get("/")
def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API funcionando"}

@app.post("/prever", response_model=PrevisaoResponse, tags=["Previsão"])
def prever_resolutividade(ocorrencia: OcorrenciaRequest) -> PrevisaoResponse:
    """
    Analisa uma ocorrência e retorna a previsão de resolutividade.
    """
    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo não disponível. Execute: python gerar_modelo.py"
        )
    
    features = np.array([[
        ocorrencia.periodo_decorrido_dias,
        ocorrencia.suspeito_conhecido,
        ocorrencia.tem_testemunhas,
        ocorrencia.tem_imagens_cameras,
        ocorrencia.suspeito_rastreavel, 
        ocorrencia.vestigios_preservados
    ]])

    # Fazer predição
    previsao_classe = modelo.predict(features)[0] # Obter a classe predita (0, 1, 2)
    probabilidades = modelo.predict_proba(features)[0] # Obter probabilidades para cada classe
    status = RESOLUTIVIDADE_CLASSES.get(previsao_classe, "Desconhecido") # Mapear para string
    confianca = probabilidades[previsao_classe] # Probabilidade da classe predita
    
    motivo = (f"Previsão baseada em modelo ML com confiança de {confianca * 100:.2f}%. "
              f"Probabilidades - Baixa: {probabilidades[0] * 100:.2f}%, "
              f"Média: {probabilidades[1] * 100:.2f}%, "
              f"Alta: {probabilidades[2] * 100:.2f}%.")
    
    return PrevisaoResponse(
        resolutividade=status,
        motivo=motivo
    )



  
