# NYATER
import os, asyncio
from models.ciscoModel import snmpPyCiscoData
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



# Cisco
async def ciscoPoolRemote(remoteIP: str, queueToInsrt: asyncio.Queue):
    print("starting work on ", remoteIP)
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        USMUSRDATA,
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

    returObj = snmpPyCiscoData()

    returObj(
        hostname="X"
    )

    returnDict = {
        "source": "CISCO",
        "value": returObj,
        "type": "snmpPyCiscoData"
    }
    # return returnObj
    await queueToInsrt.put(returnDict)