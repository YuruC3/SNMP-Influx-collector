import ipaddress, os, re, time, funct, classes
#SNMP
# from easysnmp import Session
# QoL
from typing import Annotated, Final


# Program ENV---------------------------------------
HOST_LIST: Final[list] = os.getenv("HOST_LIST")

SNMPUSER: Final[str] = os.getenv("SNMPUSER", None)
SNMPPRIVKEY: Final[str] = os.getenv("SNMPPRIVKEY", None)
SNMPAUTHKEY: Final[str] = os.getenv("SNMPAUTHKEY", None)

SNMPAUTHPROTO: Final[str] = os.getenv("SNMPAUTHPROTO", "SHA")
SNMPPRIVPROTO: Final[str] = os.getenv("SNMPPRIVPROTO", "SHA")
SNMPORT: Final[int] = os.getenv("SNMPORT", 161)

# Flightchecks-------------------------------------------

if SNMPAUTHPROTO and SNMPPRIVPROTO == "SHA":
    USMDATA = UsmUserData(
        userName=SNMPUSER,
        authKey=SNMPPRIVKEY,
        privKey=SNMPAUTHKEY,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmHMACSHAAuthProtocol,
    )
elif SNMPAUTHPROTO and SNMPPRIVPROTO == "AES128":
    USMDATA = UsmUserData(
        userName=SNMPUSER,
        authKey=SNMPPRIVKEY,
        privKey=SNMPAUTHKEY,
        authProtocol=usmAesCfb128Protocol,
        privProtocol=usmAesCfb128Protocol,
    )
elif SNMPAUTHPROTO == "SHA" and SNMPPRIVPROTO == "AES128":
    USMDATA = UsmUserData(
        userName=SNMPUSER,
        authKey=SNMPPRIVKEY,
        privKey=SNMPAUTHKEY,
        authProtocol=usmHMACSHAAuthProtocol,
        privProtocol=usmAesCfb128Protocol,
    )
elif SNMPAUTHPROTO == "AES128" and SNMPPRIVPROTO == "SHA":
    USMDATA = UsmUserData(
        userName=SNMPUSER,
        authKey=SNMPPRIVKEY,
        privKey=SNMPAUTHKEY,
        authProtocol=usmAesCfb128Protocol,
        privProtocol=usmHMACSHAAuthProtocol,
    )
else:        
    raise Exception(f"No PrivAuth option like {SNMPPRIVPROTO}")

# Helper functions
def wattageCalc(amperageInp: float, voltageInp: float) -> float:
    return amperageInp * voltageInp

# Check if some neccesary ENVs are passed
if not USEINFLUX and not USESQL:
    raise Exception("No database selected to store the data")

# if HOST_LIST empty, raise Exception No hosts passed
if not HOST_LIST:
    raise Exception("No hosts passed\nExiting...")

# for host in HOST_LIST check if valid IP and create a list with strings
for host in HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(host))
    except ValueError:
        raise Exception(f" IP {ip} is invalid.\nExiting...")

# Done under "Program ENV" on line ~18


# Code-------------------------------------------

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


async def poolRemote(remoteIP: str):
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        UsmUserData(
            userName=SNMPUSER,
            authKey=SNMPPRIVKEY,
            privKey=SNMPAUTHKEY,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmHMACSHAAuthProtocol,
        ),
        await UdpTransportTarget.create((remoteIP, SNMPORT)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()


# tasks = [poolRemote(ip) for ip in HOST_LIST]
# results = await asyncio.gather(*tasks)








# Create connections for MySQL and InfluxDB

# functions for inserting data into two DBs


# DNS lookup if the user passed a hostname
# if not given a specific IP for DNS server, fallback to 1.1.1.1

# maybe a class?
# store last value and check if it wasn't sent already to the database
