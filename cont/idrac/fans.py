import os, asyncio
from models.fanModel import fanModel
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



async def idracPoolRemoteFAN_v3(remoteIP: str, queueToInsrt: asyncio.Queue) -> dict:
    snmpEngine = SnmpEngine()

    rpm_oid  = "1.3.6.1.4.1.674.10892.5.4.700.12.1.6"
    name_oid = "1.3.6.1.4.1.674.10892.5.4.700.12.1.19"

    rpms, names = await asyncio.gather(
        walk_column_v3(snmpEngine, remoteIP, rpm_oid),
        walk_column_v3(snmpEngine, remoteIP, name_oid),
    )

    snmpEngine.close_dispatcher()

    # merge by index
    out = {}
    for idx, rpm in rpms.items():
        out[idx] = {"rpm": rpm, "name": names.get(idx).split(".")[2]}

    returnDict = {
        "source": "FANS",
        "value": out,
        "type": "Dict"
    }

    await queueToInsrt.put(returnDict)