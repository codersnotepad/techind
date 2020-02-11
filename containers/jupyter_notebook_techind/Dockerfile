# docker image build -t jupyter-notebook-techind .
# docker run -v "$(pwd):/home/jovyan/techind" -p 18888:8888 --name jupyter-notebook-techind jupyter-notebook-techind

FROM jupyter/base-notebook:python-3.7.4

COPY --chown=jovyan:users requirements.txt /tmp/

USER root
RUN sudo apt-get update
RUN sudo apt-get install -y libpq-dev
RUN sudo apt-get install -y gcc
RUN sudo apt-get install -y htop

RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
