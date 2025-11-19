import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import joblib
import warnings

# Ignorar warnings de convergência do modelo, comum em exemplos simples
warnings.filterwarnings('ignore')

# Mapeamento para as classes de resolutividade
RESOLUTIVIDADE_CLASSES = {
    0: "Baixa",
    1: "Média",
    2: "Alta"
}

def treinar_e_salvar_modelo():
    """
    Simula o carregamento, pré-processamento e treinamento de um classificador
    multiclasse para prever a resolutividade de ocorrências policiais usando
    o novo conjunto de features genéricas.
    """
    print("Iniciando a simulação de treinamento do modelo multiclasse...")

    # =========================================================================
    # 1. Geração de Dados Fictícios (Substituir por dados reais)
    #    Novas Features:
    #    - periodo_registro_dias (Contínuo)
    #    - suspeito_conhecido (Binário)
    #    - tem_testemunhas (Binário)
    #    - tem_imagens_cameras (Binário)
    #    - suspeito_rastreavel (Binário)
    #    - praticado_internet (Binário)
    #    - telefone_suspeito_conhecido (Binário)
    #    - objeto_periciavel (Binário)
    # =========================================================================

    np.random.seed(42)
    data_size = 500

    # Gerar dados base
    data = pd.DataFrame({
        'periodo_registro_dias': np.random.randint(1, 60, data_size), # 1 a 60 dias
        'suspeito_conhecido': np.random.choice([0, 1], data_size, p=[0.7, 0.3]),
        'tem_testemunhas': np.random.choice([0, 1], data_size, p=[0.65, 0.35]),
        'tem_imagens_cameras': np.random.choice([0, 1], data_size, p=[0.75, 0.25]),
        'suspeito_rastreavel': np.random.choice([0, 1], data_size, p=[0.7, 0.3]),
        'praticado_internet': np.random.choice([0, 1], data_size, p=[0.8, 0.2]),
        'telefone_suspeito_conhecido': np.random.choice([0, 1], data_size, p=[0.85, 0.15]),
        'objeto_periciavel': np.random.choice([0, 1], data_size, p=[0.6, 0.4]),
        # Variável Alvo inicial: 0=Baixa, 1=Média, 2=Alta
        'resolutividade': np.random.choice([0, 1, 2], data_size, p=[0.4, 0.35, 0.25]) 
    })

    # Ajustes para introduzir correlação (Lógica Fictícia):
    
    # Condição para Alta Resolutividade (2): 
    # Suspeito conhecido E Suspeito rastreável E (Testemunhas OU Imagens) E Registro rápido (< 5 dias)
    cond_alta = (data['suspeito_conhecido'] == 1) & \
                (data['suspeito_rastreavel'] == 1) & \
                ((data['tem_testemunhas'] == 1) | (data['tem_imagens_cameras'] == 1)) & \
                (data['periodo_registro_dias'] < 5)
    
    data.loc[cond_alta, 'resolutividade'] = np.random.choice([1, 2], data[cond_alta].shape[0], p=[0.1, 0.9])
    
    # Condição para Baixa Resolutividade (0):
    # Suspeito desconhecido E Ausência de Testemunhas E Registro muito lento (> 30 dias)
    cond_baixa = (data['suspeito_conhecido'] == 0) & \
                 (data['tem_testemunhas'] == 0) & \
                 (data['periodo_registro_dias'] > 30)
    
    data.loc[cond_baixa, 'resolutividade'] = np.random.choice([0, 1], data[cond_baixa].shape[0], p=[0.8, 0.2])


    # =========================================================================
    # 2. Pré-processamento (Pipeline)
    # =========================================================================

    # Separar X (features) e y (target)
    X = data.drop('resolutividade', axis=1)
    y = data['resolutividade']

    # Todas as features são tratadas como numéricas/binárias e serão escalonadas
    colunas_features = list(X.columns)
    
    # Criar transformador: StandardScaler para todas as features
    # (Mesmo para binárias, ajuda a centralizar os dados no pipeline)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), colunas_features)
        ],
        remainder='passthrough' # Não deve haver colunas restantes
    )

    # =========================================================================
    # 3. Definição do Modelo (Regressão Logística Multiclasse)
    # =========================================================================

    # Usando Regressão Logística com multi_class='multinomial' para lidar com 3 classes
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            random_state=42,
            multi_class='multinomial', 
            solver='lbfgs', 
            max_iter=500 # Aumentar iterações para garantir convergência com mais features
        ))
    ])

    # Dividir os dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


    # =========================================================================
    # 4. Treinamento e Avaliação
    # =========================================================================

    print("\nTreinando o modelo...")
    model.fit(X_train, y_train)
    print("Treinamento concluído.")

    # Fazer previsões no conjunto de teste
    y_pred = model.predict(X_test)

    # Avaliar o desempenho
    accuracy = accuracy_score(y_test, y_pred)

    print("\n--- Avaliação do Modelo Multiclasse (Novas Features) ---")
    print(f"Acurácia no conjunto de teste: {accuracy:.4f}")
    print("\nRelatório de Classificação (Classes 0=Baixa, 1=Média, 2=Alta):")
    print(classification_report(y_test, y_pred, target_names=list(RESOLUTIVIDADE_CLASSES.values())))

    # =========================================================================
    # 5. Salvar o Modelo Treinado
    # =========================================================================
    try:
        joblib.dump(model, 'resolutividade_model_multiclass_generico.pkl')
        print("\nModelo e Pipeline salvos em 'resolutividade_model_multiclass_generico.pkl'")
    except Exception as e:
        print(f"Erro ao salvar o modelo: {e}")

    # =========================================================================
    # 6. Exemplo de Previsão em Novos Dados
    # =========================================================================

    # Cenário otimista (Alta Resolutividade)
    novo_incidente = pd.DataFrame({
        'periodo_registro_dias': [1], 
        'suspeito_conhecido': [1], 
        'tem_testemunhas': [1], 
        'tem_imagens_cameras': [0],
        'suspeito_rastreavel': [1],
        'praticado_internet': [0],
        'telefone_suspeito_conhecido': [1],
        'objeto_periciavel': [1]
    })

    # Previsão de probabilidades para todas as classes
    previsao_proba_array = model.predict_proba(novo_incidente)[0]
    previsao_classe = model.predict(novo_incidente)[0]
    
    status = RESOLUTIVIDADE_CLASSES.get(previsao_classe, "Desconhecido")

    print("\n--- Previsão de Novo Incidente (Cenário Otimista) ---")
    print(f"Dados do Incidente: {novo_incidente.to_dict(orient='records')[0]}")
    print(f"Classe Prevista: {status}")
    print("\nProbabilidades por Classe:")
    print(f"  {RESOLUTIVIDADE_CLASSES[0]}: {previsao_proba_array[0] * 100:.2f}%")
    print(f"  {RESOLUTIVIDADE_CLASSES[1]}: {previsao_proba_array[1] * 100:.2f}%")
    print(f"  {RESOLUTIVIDADE_CLASSES[2]}: {previsao_proba_array[2] * 100:.2f}%")

if __name__ == "__main__":
    treinar_e_salvar_modelo()