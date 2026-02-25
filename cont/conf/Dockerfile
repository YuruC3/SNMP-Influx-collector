FROM alpine:latest

# https://docs.docker.com/reference/dockerfile/#environment-replacement
# ENV PUID=1600
# ENV USER=itsme

# VOLUME [""]

RUN apk update && \
    apk add python3 py3-pip su-exec curl && \
    mkdir -p /app/snmpython/

WORKDIR /app/snmpython/

COPY ../code/someMain.py /app/snmpython/

# COPY ./entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Add user to run under
# RUN adduser --disabled-password -u "${PUID}" "${USER}"
# RUN chown -R "${USER}" /app/snmpython


COPY ./requirements.txt /app/snmpython/

RUN python3 -m venv venv && \
    venv/bin/python3 -m pip install --upgrade pip && \
    venv/bin/pip3 install -r requirements.txt
    # venv/bin/pip3 install -r requirements.txt 

# Set user. No need for root past this point
# USER "${USER}"

# ENTRYPOINT ["/entrypoint.sh"]

# HEALTHCHECK --interval=3s --timeout=3s --retries=3 \
#   CMD curl --fail http://127.0.0.1:8181/health || exit 1

CMD ["/app/snmpython/someMain.py"]
