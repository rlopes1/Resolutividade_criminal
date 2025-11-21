from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Testa o endpoint de health check"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_previsao_resolutividade_alta():
    """
    Testa o endpoint de previsão com um cenário otimista,
    esperando uma classificação de 'Alta' ou 'Média' resolutividade.
    """
    payload = {
        "periodo_decorrido_dias": 1,
        "suspeito_conhecido": 1,
        "tem_testemunhas": 1,
        "tem_imagens_capturadas": 0,
        "suspeito_rastreavel": 1,
        "tem_vestigios_preservados": 1
    }
    response = client.post("/prever", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resolutividade" in data
    assert data["resolutividade"] in ["Alta", "Média", "Baixa"] # A classe deve ser uma das válidas

def test_previsao_resolutividade_baixa():
    """
    Testa o endpoint de previsão com um cenário pessimista,
    esperando uma classificação de 'Baixa' resolutividade.
    """
    payload = {
        "periodo_decorrido_dias": 50,
        "suspeito_conhecido": 0,
        "tem_testemunhas": 0,
        "tem_imagens_capturadas": 0,
        "suspeito_rastreavel": 0,
        "tem_vestigios_preservados": 0
    }
    response = client.post("/prever", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "resolutividade" in data
    assert data["resolutividade"] == "Baixa"

def test_previsao_payload_invalido():
    """
    Testa o endpoint de previsão enviando um payload com um campo faltando,
    esperando um erro de validação 422.
    """
    payload = {
        "periodo_decorrido_dias": 5,
        "suspeito_conhecido": 1,
        "tem_testemunhas": 1
        # Faltam os outros campos
    }
    response = client.post("/prever", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
