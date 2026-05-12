# pybnafar 🇧🇷 - SDK de Inteligência para o SUS

**pybnafar** é uma solução de ponta para a gestão de dados da Assistência Farmacêutica no Brasil. Esta ferramenta automatiza o trabalho pesado de baixar, limpar e organizar os dados do BNAFAR, permitindo que você foque no que importa: **políticas públicas baseadas em evidências**.

---

## 🏆 Valor Estratégico para a Gestão

### 1. Previsão de Faltas (Rupturas)
O sistema detecta automaticamente municípios onde o estoque de medicamentos críticos zerou entre dois ciclos de reporte, diferenciando a "falta real" de um simples "esquecimento de digitação".

### 2. Combate ao Desperdício
Através do monitoramento de prazos de validade e pesos de criticidade (Ex: Medicamentos de Alto Custo), o sistema gera um ranking de prioridade para redistribuição de estoques próximos ao vencimento.

### 3. Governança Ética (Score de Confiança)
Não penalize gestores por dados ruins sem entender o contexto. Nosso algoritmo identifica municípios com falhas de infraestrutura (internet/pessoal) que geram dados incompletos, garantindo uma avaliação justa e técnica.

---

## 🖥️ Como Utilizar

### Interface Visual (Sem Programação)
Para quem prefere uma interface gráfica amigável:
```bash
pybnafar --dashboard
```

### Linha de Comando (Automação)
Ideal para TI e analistas de dados:
- `pybnafar --sync`: Mantém seu Data Lake local atualizado com o Ministério da Saúde.
- `pybnafar --report --ufs MG`: Gera um resumo instantâneo da saúde farmacêutica de Minas Gerais.

### Integração com a RNDS
A biblioteca gera arquivos no formato **HL7 FHIR R4**, prontos para serem integrados aos sistemas da Rede Nacional de Dados de Saúde.

---

## 📚 Documentação Adicional
- [Manual Técnico Detalhado](docs/DOCUMENTATION.md)
- [Cenário de Uso Prático](USAGE_SCENARIO.md)
- [Como Contribuir](CONTRIBUTING.md)
