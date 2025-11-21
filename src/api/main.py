from fastapi import FastAPI
from src.models.schemas import OcorrenciaRequest, PrevisaoResponse


# --- Configuração da Aplicação ---
app = FastAPI(
    title="API de Análise de Resolutividade Criminal",
    description="Prevê o potencial de resolução de uma ocorrência com base em regras de negócio.",
    version="1.1.0" # Versão ajustada para refletir a mudança de lógica
)



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
    # Contagem de evidências físicas e testemunhais
    total_evidencias = sum([
        ocorrencia.tem_testemunhas,
        ocorrencia.tem_imagens_capturadas,
        ocorrencia.tem_vestigios_preservados
    ])

    # --- Regras de Negócio para Classificação ---

    # REGRA 1: ALTA RESOLUTIVIDADE
    # Fato recente com suspeito conhecido/rastreável e alguma evidência.
    if ocorrencia.periodo_decorrido_dias <= 7 and (ocorrencia.suspeito_conhecido or ocorrencia.suspeito_rastreavel) and total_evidencias >= 1:
        return PrevisaoResponse(
            resolutividade="Alta",
            motivo="Fato recente com identificação/rastreio do suspeito e evidências disponíveis."
        )

    # REGRA 2: MÉDIA RESOLUTIVIDADE
    # Fato menos recente com suspeito conhecido, ou muitas evidências.
    if (ocorrencia.periodo_decorrido_dias <= 30 and ((ocorrencia.suspeito_conhecido or ocorrencia.suspeito_rastreavel) and total_evidencias >= 1)) or \
          total_evidencias >= 3 and ocorrencia.periodo_decorrido_dias <= 60:
        return PrevisaoResponse(
            resolutividade="Média",
            motivo="Boas pistas iniciais (suspeito conhecido ou múltiplas evidências)."
        )

    # REGRA 3: BAIXA RESOLUTIVIDADE (Default)
    # Poucas pistas ou muito tempo decorrido.
    return PrevisaoResponse(
        resolutividade="Baixa",
        motivo="Poucas pistas iniciais ou tempo decorrido elevado."
    )