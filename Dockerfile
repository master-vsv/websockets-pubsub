FROM python:3.10.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG USER=python
ARG UID=1001
ARG GID=1002
ARG MAIN_VERSION
ENV MAIN_VERSION=${MAIN_VERSION}

RUN apt update -qq && apt install -yqq curl && apt-get clean 
# && apt install libc6
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN ls -l $VIRTUAL_ENV

RUN mkdir -p home/python/.cache/Nuitka
RUN chown -R ${UID}:${GID} home/python/.cache/Nuitka

RUN mkdir -p compiled
RUN chown -R ${UID}:${GID} compiled
RUN chmod -R 764 compiled

ARG WORKDIR=/backend
WORKDIR ${WORKDIR}
COPY ./backend/ .

RUN groupadd -g ${GID} ${USER} && \
  useradd --no-create-home --no-log-init -u ${UID} -g ${GID} ${USER} && \
  chown -R ${UID}:${GID} ${WORKDIR} && \
  chown -R ${UID}:${GID} $VIRTUAL_ENV && \
  chown -R ${UID}:${GID} ./scripts/start-main.sh

USER ${USER}

RUN pip install -q --no-cache-dir --no-python-version-warning --disable-pip-version-check -r requirements.txt
RUN pip install -q --no-cache-dir --no-python-version-warning --disable-pip-version-check nuitka

# RUN sudo apt-get install python3-dev
#HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=6 CMD curl -f "${MAIN_HEALTHCHECK_URL}"
RUN chmod 755 ./scripts/start-main.sh
# RUN python ./scripts/compile.py


# RUN python ./scripts/compile.py  >> compile.txt
CMD [ "./scripts/start-main.sh" ]
