# pybnafar 🇧🇷 - SDK de Inteligência para o SUS

**pybnafar** é uma ferramenta de inovação para transformar a gestão da Assistência Farmacêutica no Brasil. Automatizamos o acesso aos dados do BNAFAR (OpenDATASUS), permitindo que gestores tomem decisões baseadas em evidências.

## 🏆 Inovação para o SUS

- **Evite o Desperdício**: Identifique medicamentos próximos ao vencimento por município.
- **Preveja a Falta**: Detecte rupturas de estoque antes que o paciente fique sem o remédio.
- **Interoperabilidade**: Gere arquivos no padrão **HL7 FHIR** para integração com a **RNDS**.
- **Ética**: Analise a qualidade do dado com o Score de Confiança, evitando preconceitos algorítmicos.

## 🖥️ Como Usar (Sem Programação)

Se você tem o **Docker** instalado, basta rodar um comando para ter o painel interativo:

```bash
docker build -t pybnafar .
docker run -p 8501:8501 -v $(pwd)/meus_dados:/app/bnafar_workspace pybnafar
```
Acesse `http://localhost:8501` no seu navegador.

## 🛠️ Linha de Comando (CLI)

```bash
# Sincroniza dados do governo
pybnafar --sync

# Abre o painel interativo (Streamlit)
pybnafar --dashboard

# Relatório de inteligência no terminal
pybnafar --report --ufs RJ MG
```

## 📚 Documentação
- [Cenário de Uso e Replicação](USAGE_SCENARIO.md)
- [Referência Técnica (Inglês)](docs/DOCUMENTATION.md)
