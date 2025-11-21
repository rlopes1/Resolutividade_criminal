from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict # Importar ConfigDict
from typing import Dict

# --- Configuração da Aplicação ---
app = FastAPI(
    title="API de Análise de Resolutividade Criminal",
    description="Prevê o potencial de resolução de uma ocorrência com base em regras de negócio.",
    version="1.1.0" # Versão ajustada para refletir a mudança de lógica
)

# --- Modelos de Dados (Pydantic) ---

class Ocorrencia(BaseModel):
    """Define a estrutura de dados de entrada para uma ocorrência."""
    periodo_decorrido_dias: int = Field(..., ge=0, description="Dias desde o fato.")
    suspeito_conhecido: bool = Field(..., description="O suspeito foi identificado?")
    tem_testemunhas: bool = Field(..., description="Há testemunhas do fato?")   
    tem_imagens_cameras: bool = Field(..., description="Há imagens de câmeras?")
    suspeito_rastreavel: bool = Field(..., description="O suspeito pode ser rastreado?")
    vestigios_preservados: bool = Field(..., description="Vestígios foram preservados para perícia?")

    # --- CORREÇÃO: Atualização para o padrão Pydantic V2 ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "periodo_decorrido_dias": 2,
                "suspeito_conhecido": True,
                "tem_testemunhas": True,
                "tem_imagens_cameras": False,
                "suspeito_rastreavel": True,
                "vestigios_preservados": True
            }
        }
    )

class PrevisaoResponse(BaseModel):
    """Define a estrutura de dados da resposta da previsão."""
    resolutividade: str
    motivo: str

# --- Endpoints da API ---

@app.get("/", include_in_schema=True)
def health_check() -> Dict[str, str]:
    """Verifica se a API está em execução."""
    return {"status": "ok"}

@app.post("/prever", response_model=PrevisaoResponse, tags=["Previsão"])
def prever_resolutividade(ocorrencia: Ocorrencia) -> PrevisaoResponse:
    """
    Analisa uma ocorrência e retorna a previsão de resolutividade.
    """
    # Contagem de evidências físicas e testemunhais
    total_evidencias = sum([
        ocorrencia.tem_testemunhas,
        ocorrencia.tem_imagens_cameras,
        ocorrencia.vestigios_preservados
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
    if (ocorrencia.periodo_decorrido_dias <= 30 and ocorrencia.suspeito_conhecido) or total_evidencias >= 2:
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