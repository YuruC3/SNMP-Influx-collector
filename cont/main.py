import ipaddress, os, re, time, funct, classes, asyncio
# SNMP
from pysnmp.hlapi.v3arch.asyncio import *
# QoL
from typing import Annotated, Final
# functions
from funct import *
# additional classes
from classes import *

# Program ENV---------------------------------------
ROUND_PREC: Final[int] = os.getenv("ROUND_PREC", 6)
IDRAC_HOST_LIST: Final[list] = os.getenv("IDRAC_HOST_LIST").split(";")
CISCO_HOST_LIST: Final[list] = os.getenv("CISCO_HOST_LIST").split(";")

SNMPUSER: Final[str] = os.getenv("SNMPUSER", None)
SNMPPRIVKEY: Final[str] = os.getenv("SNMPPRIVKEY", None)
SNMPAUTHKEY: Final[str] = os.getenv("SNMPAUTHKEY", None)

# Right now I'll only use SHA
# SNMPAUTHPROTO: Final[str] = os.getenv("SNMPAUTHPROTO", "SHA")
# SNMPPRIVPROTO: Final[str] = os.getenv("SNMPPRIVPROTO", "SHA")
SNMPORT: Final[int] = os.getenv("SNMPORT", 161)

# Flightchecks-------------------------------------------
# Check if SNMP ENV are empty
if not SNMPUSER or not SNMPPRIVKEY or not SNMPAUTHKEY:
    raise Exception("No SNMP user or/and PrivAuth passed")

# if HOST_LIST empty, raise Exception No hosts passed
if not IDRAC_HOST_LIST and not CISCO_HOST_LIST:
    raise Exception("No hosts passed\nExiting...")

# for host in HOST_LIST check if valid IP and create a list with strings
for idracHost in IDRAC_HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(idracHost))
    except ValueError:
        raise Exception(f" IP {ip} for IDRAC devices is invalid.\nExiting...")
for ciscoHost in CISCO_HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(ciscoHost))
    except ValueError:
        raise Exception(f" IP {ip} for Cisco devices is invalid.\nExiting...")

# Done under "Program ENV" on line ~18


# Code-------------------------------------------

# Helper functions
def wattageCalc(amperageInp: float, voltageInp: float) -> float:
    return amperageInp * voltageInp


async def ciscoPoolRemote(remoteIP: str):
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
        # Get Hostname
        ObjectType(ObjectIdentity(".1.3.6.1.2.1.1.5.0")),
        # 
    )

    print(iterator)

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

async def idracPoolRemote(remoteIP: str):
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
        # Get Hostname
        ObjectType(ObjectIdentity(".1.3.6.1.2.1.1.5.0")),
        # 
    )

    print(iterator)

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


async def idracPoolRemote_v1(remoteIP: str):
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        # SNMPv1 = mpModel=0 (SNMPv2c would be mpModel=1)
        CommunityData("public", mpModel=0),
        await UdpTransportTarget.create((remoteIP, SNMPORT)),
        ContextData(),
        # Hostname (sysName.0)
        ObjectType(ObjectIdentity(".1.3.6.1.2.1.1.5.0")),                            #0

        # PSU1 powerDraw and PSU2 powerDraw (Amps)
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.1")),    #1
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.2")),    #2
        # (Volts)
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.31")),    #3
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.32")),    #4

        # Get Inlet, Exhaust, CPU1, CPU2
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.1")),    #5
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.2")),    #6
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.3")),    #7
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.4")),    #8

        # Uptime in seconds
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.2.5.0")),    #9
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
        for oid, val in varBinds:
            print(f"{oid.prettyPrint()} = {val.prettyPrint()}")

    # for element in varBinds:
    #     print(element)

    snmpEngine.close_dispatcher()
    # print(varBinds[1][-1])
    # print(type(varBinds[1][-1]))
    returnObj = snmpPyIDRACData(
        hostname=varBinds[0][-1], 
        # Hostname

        powerDrawPSU1=round((int(varBinds[1][-1]) / 10) * (int(varBinds[3][-1]) / 1000), ROUND_PREC),
        powerDrawPSU2=round((int(varBinds[2][-1]) / 10) * (int(varBinds[4][-1]) / 1000), ROUND_PREC),
        # PSU1 and PSU2 power draw in Watts

        voltagePSU1=round((int(varBinds[3][-1]) / 1000), ROUND_PREC),
        voltagePSU2=round((int(varBinds[4][-1]) / 1000), ROUND_PREC),
        # PSU1 and PSU2 voltages

        inletTemp=int(varBinds[5][-1] / 10),
        exhaustTemp=int(varBinds[6][-1] / 10),
        # Inlet and Exhaust temp

        cpu1Temp=int(varBinds[7][-1] / 10),
        cpu2Temp=int(varBinds[8][-1] / 10),
        # CPU1 and CPU2 temp

        uptimeH=round(((int(varBinds[9][-1]) / 60) / 60), ROUND_PREC),
        # seconds->minutes->hours
        uptimeD=round((((int(varBinds[9][-1]) / 60) / 60) / 24), ROUND_PREC)
        # seconds->minutes->hours->days
    )


    return returnObj


yes = asyncio.run(idracPoolRemote_v1("192.168.20.7"))

print("for loop")
print(yes)

x = idracFanStatus(6)
# print(yes.hostname)
# print(yes.powerDrawPSU1)
# print(yes.powerDrawPSU2)
# print(yes.voltagePSU1)
# print(yes.voltagePSU2)
# print(yes.inletTemp)
# print(yes.exhaustTemp)
# print(yes.uptimeH)
# print(yes.uptimeD)


# poolRemote(HOST_LIST[0])
# while True:
#     tasks = [poolRemote(ip) for ip in HOST_LIST]
#     results = await asyncio.gather(*tasks)

#     print(results)

#     await asyncio.sleep(20)








# Create connections for MySQL and InfluxDB

# functions for inserting data into two DBs


# DNS lookup if the user passed a hostname
# if not given a specific IP for DNS server, fallback to 1.1.1.1

# maybe a class?
# store last value and check if it wasn't sent already to the database

