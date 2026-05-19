# Configurações de Rede
OPENDATASUS_CKAN_API = (
    "https://opendatasus.saude.gov.br/api/3/action/package_show?id=bnafar-estoque"
)
OPENDATASUS_URL = "https://opendatasus.saude.gov.br/dataset/bnafar-estoque"

# Pesos para o Índice de Confiabilidade de Dados (ICD)
# Estes valores devem ser calibrados via consenso de especialistas (Método Delphi)
WEIGHTS = {"temporal_consistency": 0.4, "network_coverage": 0.4, "recency": 0.2}

# Pesos de Criticidade de Medicamentos (Baseado em Complexidade SUS)
CRITICALITY_WEIGHTS = {
    "E": 3,  # Componente Especializado (Alto Custo/Complexidade)
    "S": 2,  # Componente Estratégico
    "B": 1,  # Componente Básico
    "O": 1,  # Outros
}
