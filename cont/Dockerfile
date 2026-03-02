FROM alpine:latest

# https://docs.docker.com/reference/dockerfile/#environment-replacement
# ENV PUID=1600
# ENV USER=itsme
# VOLUME [""]

RUN apk update && \
    apk add python3 py3-pip su-exec curl 

RUN adduser -D -s /bin/sh -u 1600 pyusr
RUN mkdir -p /app/snmpython/ && \
    chown -R 1600:1600 /app/snmpython/ 
USER pyusr    

WORKDIR /app/snmpython/

COPY ./requirements.txt /app/snmpython/
RUN python3 -m venv pyvenv && \
    pyvenv/bin/python3 -m pip install --upgrade pip && \
    pyvenv/bin/pip3 install -r requirements.txt

COPY ./mainRE.py /app/snmpython/

RUN mkdir cisco db idrac models snmp

ADD cisco /app/snmpython/cisco
ADD db /app/snmpython/db
ADD idrac /app/snmpython/idrac
ADD models /app/snmpython/models
ADD snmp /app/snmpython/snmp

    # COPY ../code/MIBs/ /app/snmpython/MIBs

# COPY ./entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Add user to run under
# RUN adduser --disabled-password -u "${PUID}" "${USER}"
# RUN chown -R "${USER}" /app/snmpython


    # venv/bin/pip3 install -r requirements.txt 

# Set user. No need for root past this point
# USER "${USER}"

# ENTRYPOINT ["/entrypoint.sh"]

# HEALTHCHECK --interval=3s --timeout=3s --retries=3 \
#   CMD curl --fail http://127.0.0.1:8181/health || exit 1

CMD ["/app/snmpython/pyvenv/bin/python3", "/app/snmpython/mainRE.py"]
