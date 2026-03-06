import asyncio, os
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






# Return a following object

# {
#     1: "SomeObject",
#     2: "someOtherObject"
# }

# The value is always a string so it needs to be converted to int if needed

async def walk_column_v3(snmpEngine, remoteIP: str, base_oid: str) -> dict:
    rows = {}
    async for errInd, errStat, errIdx, varBinds in walk_cmd(
        snmpEngine,
        USMUSRDATA,
        await UdpTransportTarget.create((remoteIP, SNMPORT)),
        ContextData(),
        ObjectType(ObjectIdentity(base_oid)),
        lexicographicMode=False,
    ):
        if errInd:
            print(f"\n\n{errInd}\n\n")
            if "No SNMP response received before timeout" in errInd:
                print(f"Host {remoteIP} timed out.\nContinuing...")
                return 1
            raise RuntimeError(errInd)
        if errStat:
            raise RuntimeError(errStat.prettyPrint())

        for oid, val in varBinds:
            # index is typically the last sub-identifier
            idx = int(oid.prettyPrint().split(".")[-1])
            rows[idx] = val.prettyPrint()

    return rows