from fastapi import FastAPI, HTTPException
from src.models.schemas import OcorrenciaRequest
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Resolutividade Criminal",)

@app.get("/")
def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API funcionando"}

@app.post("/resolutividade")
def resolutividade_criminal(dados: OcorrenciaRequest):
    
    """
    Calcula a resolutividade de uma ocorrência com base nos dados fornecidos.
    Entenda-se resolutividade como a probabilidade de resolução do caso com base em fatores como
    tempo decorrido, suspeito conhecido, testemunhas, imagens e vestígios.  
    """
    try:
        razoes = []

        evidencias_suficientes = sum([
            dados.tem_testemunhas,
            dados.tem_imagens_capturadas,
            dados.tem_vestigios_preservados
        ])
       
        # Regra 1: Alta resolutividade
            # Se o período decorrido for menor que 5 dias e o suspeito for conhecido
            # com pelo menos 1 evidência, ou se o suspeito for rastreável com pelo menos 2 evidências
        if (dados.periodo_decorrido_dias <= 5 and
            ((dados.suspeito_conhecido and             
             evidencias_suficientes >= 1) or (dados.suspeito_rastreavel and
              evidencias_suficientes >= 2))):
           
           razoes.append("Evidências suficientes com suspeito conhecido ou rastreável em prazo curto")
           result = {
               "resolutividade": "Alta",
               "razoes": razoes
           }

        # Regra 2: Média resolutividade
            # Se o período decorrido for menor que 30 dias e o suspeito for conhecido
            # ou rastreável com pelo menos 1 evidência, ou se houver pelo menos 3 evidências e o período decorrido for menor que 60 dias
        elif ((dados.periodo_decorrido_dias < 30 and
              (dados.suspeito_conhecido or 
              (dados.suspeito_rastreavel and evidencias_suficientes >= 1))) or
                evidencias_suficientes >= 3 and dados.periodo_decorrido_dias < 60):
           
           razoes.append("Evidências moderadas com suspeito conhecido ou rastreável em prazo razoável")
           result = {
               "resolutividade": "Média",
               "razoes": razoes
           }
              
        else:
        # Regra 3: Baixa resolutividade
            result = {
                "resolutividade": "Baixa",
                "razoes": ["Fatores insuficientes para alta resolutividade"]
            }
           

        
        logger.info(f"Cálculo realizado: {dados} => {result}")
        return result
        
       
        
    except Exception as e:
        logger.error(f"Erro ao calcular: {e}")
        raise HTTPException(status_code=500, detail=str(e))
