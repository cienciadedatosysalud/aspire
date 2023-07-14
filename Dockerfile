FROM node:16.20.0-alpine3.17 AS ui_development
WORKDIR /usr/src/app
COPY gui_aspire ./
RUN npm install
RUN npm run build

FROM mambaorg/micromamba:1.4.8-bullseye-slim
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml \
    && micromamba clean --all --yes \
    && rm -rf /opt/conda/conda-meta /tmp/env.yaml

COPY --from=ui_development --chown=$MAMBA_USER:$MAMBA_USER /usr/src/app/front /home/mambauser/front
COPY --chown=$MAMBA_USER:$MAMBA_USER api_aspire /home/$MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER projects /home/$MAMBA_USER/projects

ENV APP_PORT=3000
ENV APP_HOST=0.0.0.0
EXPOSE 3000

WORKDIR /home/$MAMBA_USER
CMD ["python", "./main.py"]


