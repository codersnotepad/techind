# docker image build -t techind-jn-01 .
# docker run -v "$(pwd):/home/jovyan/CPU" -p 18888:8888 --name techind-jn-01 techind-jn-01

FROM jupyter/base-notebook:python-3.7.4

COPY --chown=jovyan:users requirements.txt /tmp/

USER root
RUN sudo apt-get update
RUN sudo apt-get install -y libpq-dev
RUN sudo apt-get install -y gcc
RUN sudo apt-get install -y htop
RUN sudo apt-get install -y nano

RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple \
    techind==0.0.6

RUN ln -sv /home/jovyan/CPU /mnt/ns01
