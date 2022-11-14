ARG watchdog_version=0.8.4
ARG python_version=3.8
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/of-watchdog:${watchdog_version} as watchdog
FROM mambaorg/micromamba:latest

USER root
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE
ARG CHANNEL=pytorch

RUN mkdir -p /home/app/function/
RUN chown -R mambauser /home/
ENV HOME /home/app


RUN apt-get update \
    && apt-get -y install ca-certificates curl bzip2 ${ADDITIONAL_PACKAGE}

COPY env.yaml /tmp/env.yaml
# specific modules
COPY function/requirements.yaml /tmp/requirements.yaml

RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba install -y -n base -f /tmp/requirements.yaml && \
    micromamba clean --all --yes

RUN apt-get -qq -y remove curl \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

# Add non root user
WORKDIR /home/app/
USER mambauser
COPY index.py           .


RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/ .

ARG TEST_COMMAND="tox --current-env"
ARG TEST_ENABLED=false
RUN if [ "x$TEST_ENABLED" = "xfalse" ]; then \
    echo "skipping tests";\
    else \
    eval "$TEST_COMMAND"; \
    fi

WORKDIR /home/app/

# Set environment variables
ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV function_root="/home/app/function"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
