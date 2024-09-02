FROM node:22-alpine AS ui_development
WORKDIR /usr/src/app
COPY gui_aspire ./
RUN npm install
RUN npm run build

FROM mambaorg/micromamba:1.4.8-bullseye-slim

USER root

ARG aspire_version="Non-versioned"
ENV ASPIRE_VERSION=$aspire_version

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

ARG QUARTO_VERSION="1.5.57"
RUN curl -o quarto-linux-amd64.deb -L https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb \
    && gdebi --non-interactive quarto-linux-amd64.deb \
    && rm quarto-linux-amd64.deb \
    && apt remove -y curl gdebi-core

USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba create -y -f /tmp/env.yaml \
    && micromamba run -n aspire pip uninstall -y tangled_up_in_unicode \
    && micromamba clean --all --yes \
    && rm -rf /opt/conda/conda-meta /tmp/env.yaml

RUN echo "micromamba activate aspire" >> ~/.bashrc
RUN echo "export PATH=/opt/conda/envs/aspire/bin:${PATH}"  >> ~/.bashrc

COPY --from=ui_development --chown=$MAMBA_USER:$MAMBA_USER /usr/src/app/front /home/mambauser/front
COPY --chown=$MAMBA_USER:$MAMBA_USER api_aspire /home/$MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER projects /home/$MAMBA_USER/projects

COPY --chown=$MAMBA_USER:$MAMBA_USER entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

ENV APP_PORT=3000
ENV APP_HOST=0.0.0.0
EXPOSE 3000

WORKDIR /home/$MAMBA_USER
ENTRYPOINT ["micromamba","run","-n","aspire","/opt/entrypoint.sh"]


