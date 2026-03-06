import os, asyncio
from models.idracModel import snmpPyIDRACData
from snmp.walker import walk_column_v3
from typing import Annotated, Final

# SNMP
from pysnmp.hlapi.v3arch.asyncio import *

# SNMP ENV-------------------------------------------
ROUND_PREC: Final[int] = int(os.getenv("ROUND_PREC", 2))

SNMPUSER: Final[str] = os.getenv("SNMPUSER", None)
SNMPPRIVKEY: Final[str] = os.getenv("SNMPPRIVKEY", None)
SNMPAUTHKEY: Final[str] = os.getenv("SNMPAUTHKEY", None)
# Right now I'll only use SHA
# SNMPAUTHPROTO: Final[str] = os.getenv("SNMPAUTHPROTO", "SHA")
# SNMPPRIVPROTO: Final[str] = os.getenv("SNMPPRIVPROTO", "SHA")
SNMPORT: Final[int] = int(os.getenv("SNMPORT", 161))


# Check if SNMP ENV are empty
if not SNMPUSER or not SNMPPRIVKEY or not SNMPAUTHKEY:
    raise Exception("No SNMP user or/and PrivAuth passed")


# SNMP
USMUSRDATA = UsmUserData(
            userName=SNMPUSER,
            authKey=SNMPAUTHKEY,
            privKey=SNMPPRIVKEY,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol,
        )





# IDRAC78 get data for snmpPyIDRACData class
async def idrac7_8PoolRemote_v3(remoteIP: str, queueToInsrt: asyncio.Queue):
    print("starting work on ", remoteIP)

    snmpEngine = SnmpEngine()
    # try CPU2 as CPU1 is always there 

    mainIterator = get_cmd(
        snmpEngine,
        # SNMPv1 = mpModel=0 (SNMPv2c would be mpModel=1)
        # CommunityData("public", mpModel=0),
        USMUSRDATA,
        await UdpTransportTarget.create((remoteIP, SNMPORT)),
        ContextData(),
        # Hostname (sysName.0)
        ObjectType(ObjectIdentity(".1.3.6.1.2.1.1.5.0")),                            #0
        # Uptime in seconds
        ObjectType(ObjectIdentity(".1.3.6.1.4.1.674.10892.5.2.5.0")),    #1
    )

    errorIndication, errorStatus, errorIndex, mainVarBinds = await mainIterator

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and mainVarBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for oid, val in mainVarBinds:
            print(f"{oid.prettyPrint()} = {val.prettyPrint()}")


    # Get PSU1 current, [PSU2 current], total board power draw in watts
    currentsCurrentResults = await walk_column_v3(snmpEngine, remoteIP, ".1.3.6.1.4.1.674.10892.5.4.600.30.1.6")
    # PSU1 OID name, [PSU2 OID name], system board power draw 
    currentsNamesResults = await walk_column_v3(snmpEngine, remoteIP, ".1.3.6.1.4.1.674.10892.5.4.600.30.1.8")

    # Inlet OID name .1, [Exhaust OID name], CPU1 temp OID name, [CPU2 tempOID name]
    sensorNamesResults = await walk_column_v3(snmpEngine, remoteIP, ".1.3.6.1.4.1.674.10892.5.4.700.20.1.8")
    # Inlet temp, [Exhaust temp], CPU1 temp, [CPU2 temp]
    sensorValuesResults = await walk_column_v3(snmpEngine, remoteIP, ".1.3.6.1.4.1.674.10892.5.4.700.20.1.6")

    # .1.3.6.1.4.1.674.10892.5.4.600.20.1.6.1
    voltResult = await walk_column_v3(snmpEngine, remoteIP, ".1.3.6.1.4.1.674.10892.5.4.600.20.1.6.1")

    hasExhaust = any("exhaust" in str(thing).lower() for thing in sensorNamesResults.values())
    hasCPU2 = any("cpu2" in str(thing).lower() for thing in sensorNamesResults.values())
    hasPSU2 = any("ps2" in str(thing).lower() for thing in currentsNamesResults.values())

    snmpEngine.close_dispatcher()

    # Exhaust CPU1 and CPU2 temp

    exhaustTemp = None
    cpu2Temp = None
    if len(currentsCurrentResults) == 1 and int(mainVarBinds[1][-1]) == 0:
        exhaustTemp = int(sensorValuesResults[2]) / 10
        cpu1Temp = None
    elif hasExhaust and hasCPU2:
        exhaustTemp = int(sensorValuesResults[2]) / 10
        cpu1Temp = int(sensorValuesResults[3]) / 10
        cpu2Temp = int(sensorValuesResults[4]) / 10
    elif hasExhaust and not hasCPU2:
        exhaustTemp = int(sensorValuesResults[2]) / 10
        cpu1Temp = int(sensorValuesResults[3]) / 10
    elif hasCPU2 and not hasExhaust:
        cpu1Temp = int(sensorValuesResults[3]) / 10
        cpu2Temp = int(sensorValuesResults[4]) / 10
    else: 
        cpu1Temp = int(sensorValuesResults[2]) / 10
       
    # If power draw is 0; I.E. if server is turned off
    if len(currentsCurrentResults) == 1 and int(mainVarBinds[1][-1]) == 0:
        returnObj = snmpPyIDRACData(
            hostname=mainVarBinds[0][-1], 
            # Hostname

            powerDrawPSU1=None,
            powerDrawPSU2=None,
            # PSU1 and PSU2 power draw in Watts

            # board power draw
            powerDrawBoard=None,

            voltagePSU1=None,
            voltagePSU2=None,
            # PSU1 and PSU2 voltages

            inletTemp=(int(sensorValuesResults[1]) / 10),
            exhaustTemp=exhaustTemp,
            # Inlet and Exhaust temp

            cpu1Temp=None,
            cpu2Temp=None,
            # CPU1 and CPU2 temp

            uptimeS=int(mainVarBinds[1][-1]),
            # seconds
            uptimeH=round(((int(mainVarBinds[1][-1]) / 60) / 60), ROUND_PREC),
            # seconds->minutes->hours
            uptimeD=round((((int(mainVarBinds[1][-1]) / 60) / 60) / 24), ROUND_PREC)
            # seconds->minutes->hours->days
        )
        returnDict = {
            "source": "IDRAC",
            "value": returnObj,
            "type": "snmpPyIDRACData"
        }
        # return returnObj
        await queueToInsrt.put(returnDict)  
        return 1


    voltList = []
    for thing in voltResult:
        voltList.append(voltResult[thing])

    # PSU2 values and board power
    psu2PowerDraw = None
    psu2Amperage = None
    psu2Voltage = None

    if hasPSU2:
        psu2PowerDraw = round((int(currentsCurrentResults[2]) / 10) * (int(voltList[1]) / 1000), ROUND_PREC)
        psu2Amperage = int(currentsCurrentResults[2]) / 10
        psu2Voltage = round((int(voltList[1]) / 1000), ROUND_PREC)
        boardPowerDraw = int(currentsCurrentResults[3])
    else:
        boardPowerDraw = int(currentsCurrentResults[2])


    returnObj = snmpPyIDRACData(
        hostname=mainVarBinds[0][-1], 
        # Hostname

        powerDrawPSU1=round((int(currentsCurrentResults[1]) / 10) * (int(voltList[0]) / 1000), ROUND_PREC),
        powerDrawPSU2=psu2PowerDraw,
        # PSU1 and PSU2 power draw in Watts

        # board power draw
        powerDrawBoard=boardPowerDraw,

        voltagePSU1=round((int(voltList[0]) / 1000), ROUND_PREC),
        voltagePSU2=psu2Voltage,
        # PSU1 and PSU2 voltages

        inletTemp=(int(sensorValuesResults[1]) / 10),
        exhaustTemp=exhaustTemp,
        # Inlet and Exhaust temp

        cpu1Temp=cpu1Temp,
        cpu2Temp=cpu2Temp,
        # CPU1 and CPU2 temp

        uptimeS=int(mainVarBinds[1][-1]),
        # seconds
        uptimeH=round(((int(mainVarBinds[1][-1]) / 60) / 60), ROUND_PREC),
        # seconds->minutes->hours
        uptimeD=round((((int(mainVarBinds[1][-1]) / 60) / 60) / 24), ROUND_PREC)
        # seconds->minutes->hours->days
    )

    returnDict = {
        "source": "IDRAC",
        "value": returnObj,
        "type": "snmpPyIDRACData"
    }
    # return returnObj
    await queueToInsrt.put(returnDict)