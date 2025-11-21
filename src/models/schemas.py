from pydantic import BaseModel, Field

class OcorrenciaRequest(BaseModel):
    
    periodo_decorrido_dias: int = Field(...,ge=0, description="Número de dias do fato até o registro da ocorrência")
    suspeito_conhecido: bool = Field(..., description="Se o suspeito foi identificado")
    tem_testemunhas: bool = Field(..., description="Se há testemunhas do fato")
    tem_imagens_capturadas: bool = Field(..., description="Se há imagens capturadas do fato")
    suspeito_rastreavel: bool = Field(..., description="Se o suspeito é rastreável")
    tem_vestigios_preservados: bool = Field(..., description="Se há vestígios preservados para perícia")
    
    class Config:
        schema_extra = {
            "example": {
                "periodo_decorrido_dias": 5,
                "suspeito_conhecido": True,
                "tem_testemunhas": False,
                "tem_imagens_capturadas": True,
                "suspeito_rastreavel": True,
                "tem_vestigios_preservados": False
            }
        }


    

    
  
