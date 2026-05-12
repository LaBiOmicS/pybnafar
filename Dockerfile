FROM mambaorg/micromamba:1.5.8

COPY --chown=$MAMBA_USER:$MAMBA_USER pybnafar/environment.yml /tmp/environment.yml
COPY --chown=$MAMBA_USER:$MAMBA_USER . /app

WORKDIR /app

# Instala as dependências usando micromamba
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Configura o ambiente
ARG MAMBA_DOCKERFILE_ACTIVATE=1
ENV PATH="/opt/conda/bin:$PATH"

# Porta do Streamlit
EXPOSE 8501

# Workspace (Volume para persistência)
USER root
RUN mkdir -p /app/bnafar_workspace && chown -R $MAMBA_USER:$MAMBA_USER /app/bnafar_workspace
VOLUME /app/bnafar_workspace
USER $MAMBA_USER

# Comando de execução
ENTRYPOINT ["micromamba", "run", "-n", "base", "streamlit", "run", "pybnafar/examples/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--", "--workspace", "/app/bnafar_workspace"]
