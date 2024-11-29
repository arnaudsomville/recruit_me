FROM continuumio/anaconda3:main

# Étape 1 : Mettre à jour les outils système
USER root
RUN apt-get update && apt-get install -y \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash dockeruser
COPY --chown=dockeruser:dockeruser . /app
RUN chown -R dockeruser:dockeruser /app

# Étape 2 : Configurer l'environnement Conda et installer les dépendances
WORKDIR /app
RUN conda update -n base -c defaults conda && \
    conda create -n docker_env python=3.11 -y && \
    /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate docker_env && \
    ls && pip install pdm==2.20.1 && pdm install -v"

# Étape 3 : Créer un utilisateur non-root

USER dockeruser 
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate docker_env && \
    pdm run verify_home_folder"

EXPOSE 8080
CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate docker_env && fastapi run src/recruit_me/api/main_api.py --port=8080"]