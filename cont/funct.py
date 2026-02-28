import influxdb_client, sqlalchemy, random, os, asyncio
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from sqlalchemy import create_engine, exc  # , Column, Integer, String, Numeric
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from classes import *
from typing import Annotated, Final

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions

# SNMP
from pysnmp.hlapi.v3arch.asyncio import *

# FluxQL ENV----------------------------------------
USEINFLUX: Final[int] = int(os.getenv("USEINFLUX", 1))
if USEINFLUX:
    INFLXDBTOKEN: Final[str] = os.getenv("INFLXDBTOKEN", "123" )
    INFLUXBCKT: Final[str] = os.getenv("INFLUXBCKT", "SNMPyth")
    INFLUXORG: Final[str] = os.getenv("INFLUXORG", "staging")
    INFLXDBURL: Final[str] = os.getenv("INFLXDBURL", "http://localhost:8086")
    INFXLUXDB_MEASUEREMENT: Final[str] = os.getenv("INFXLUXDB_MEASUEREMENT", "SNMPyth-containrr")
    INFLX_SEPARATE_POINTS: Final[float] = float(os.getenv("INFLX_SEPARATE_POINTS", 0.1))
# SQL ENV-------------------------------------------
USESQL: Final[int] = int(os.getenv("USESQL", 0))
if USESQL:
    DBENGINE: Final[str] = os.getenv("DBENGINE", "mysql+asyncmy")
    DBADDR: Final[str] = os.getenv("DBADDR", "127.0.0.1")
    DBUSR: Final[str] = os.getenv("DBUSR", "root")
    DBPWD: Final[str] = os.getenv("DBPWD", "6767")
    DBNAME: Final[str] = os.getenv("DBNAME", "TEMP_SENSR")
# SNMP ENV-------------------------------------------
ROUND_PREC: Final[int] = int(os.getenv("ROUND_PREC", 6))

SNMPUSER: Final[str] = os.getenv("SNMPUSER", None)
SNMPPRIVKEY: Final[str] = os.getenv("SNMPPRIVKEY", None)
SNMPAUTHKEY: Final[str] = os.getenv("SNMPAUTHKEY", None)
# Right now I'll only use SHA
# SNMPAUTHPROTO: Final[str] = os.getenv("SNMPAUTHPROTO", "SHA")
# SNMPPRIVPROTO: Final[str] = os.getenv("SNMPPRIVPROTO", "SHA")
SNMPORT: Final[int] = int(os.getenv("SNMPORT", 161))

# Flightchecks-------------------------------------------    
# Check if some neccesary ENVs are passed
if not USEINFLUX and not USESQL:
    raise Exception("No database selected to store the data")
# Check if SNMP ENV are empty
if not SNMPUSER or not SNMPPRIVKEY or not SNMPAUTHKEY:
    raise Exception("No SNMP user or/and PrivAuth passed")


# Prepare-------------------------------------------
# INFLUX
if USEINFLUX:
    fluxdb_client = influxdb_client.InfluxDBClient(url=INFLXDBURL, token=INFLXDBTOKEN, org=INFLUXORG)
    write_fluxdb_api = fluxdb_client.write_api(write_options=ASYNCHRONOUS)
    query_fluxdb_api = fluxdb_client.query_api()
else:
    fluxdb_client = write_fluxdb_api = query_fluxdb_api = None
# SQL
if USESQL:
    engine = create_async_engine(
        f"{DBENGINE}://{DBUSR}:{DBPWD}@{DBADDR}/{DBNAME}",
        # pool_pre_ping=True,         # Check connection liveness before using and if needed, recconect
        # pool_recycle=3600,           # recycle connections older than N (3600 in this case) seconds
        echo=True,
    )    
else:
    engine = None    

# SNMP
USMUSRDATA = UsmUserData(
            userName=SNMPUSER,
            authKey=SNMPAUTHKEY,
            privKey=SNMPPRIVKEY,
            authProtocol=usmHMACSHAAuthProtocol,
            privProtocol=usmAesCfb128Protocol,
        )

# DB functions-------------------------------------------

async def sqlDataWriter(
    inpDict: dict
    ) -> int:

    # inputQueue have multiple such Dicts
    # {
    #     "source": "IDRAC",
    #     "value": returnObj,
    #     "type": "snmpPyIDRACData"
    # }
    if engine is None:
        return 3
    try: 
        async with engine.begin() as eng:
            match inpDict["source"]:

                case "CISCO":
                    await eng.execute(
                        # changeMeLater
                        t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
                    )
                case "IDRAC":
                    await eng.execute(
                        # changeMeLater
                        t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
                    )
                case "FANS":
                    await eng.execute(
                        # changeMeLater
                        t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}]
                    )

                case _:
                    print(f"No such source of data as {inpDict['source']}")
                    return 1

    except Exception as e: 
        print(e)
        return 2
    
    return 0
        
        # asyncio.sleep(5)


async def fluxWriter(
    inpDict: dict
    ) -> int:

    """
    Insert temperature data into InfluxDB
    :inputQueue: Asyncio Queue that has what is needed to be sent
    """
    # inputQueue have multiple such Dicts
    # {
    #     "source": "IDRAC",
    #     "value": returnObj,
    #     "type": "snmpPyIDRACData"
    # }

    if write_fluxdb_api is None:
        return 2

    # Prep InfluxDB data
    inflxdb_Data_To_Send = (
    influxdb_client.Point(f"{INFXLUXDB_MEASUEREMENT}")
    .tag("PLACE", inpayload.name)
    .tag("TEMP", sensorIDinp)
    .tag("TEMP", whatTheSensor)
    .field("TEMP", inpayload.temp)
    .field("TEMP", inpayload.humid)
    .field("TEMP", inpayload.hicc)
    .field("TEMP", inpayload.presss)
    .field("TEMP", inpayload.alttd)
    )

    try:
        write_fluxdb_api.write(bucket=INFLUXBCKT, org=INFLUXORG, record=inflxdb_Data_To_Send)
    except Exception as e:
        print(e)
        return 1

    return 0
    # return {"STATUS": "succesfully inserted to InfluxDB"}

            
async def ALLdbWriter(inputQueue: asyncio.Queue) -> None:
    while True:

        qu = await inputQueue.get()

        try:
            if USESQL:
                sqlResult = await sqlDataWriter(qu)
                match sqlResult:
                    case 1:
                        print("Wrong source")
                    case 2:
                        print("Error inserting to database")
                    case 3:
                        print("No engine defined")
                    case _:
                        print("nice")
            if USEINFLUX:
                fluxResult = await fluxWriter(qu)
                match fluxResult:
                    case 1:
                        print("could not insert")
                    case 2:
                        print("Error with initializing Inxlux variables")
                    case _:
                        print("nice")
        except Exception as e:
            print(e)
        finally:
            inputQueue.task_done()



# SNMP functions-------------------------------------------

# Helper functions
# def wattageCalc(amperageInp: float, voltageInp: float) -> float:
#     return amperageInp * voltageInp

# Cisco
async def ciscoPoolRemote(remoteIP: str, queueToInsrt: asyncio.Queue):
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
    queueToInsrt.put(returnDict)

# IDRAC get data for snmpPyIDRACData class
async def idracPoolRemote_v3(remoteIP: str, queueToInsrt: asyncio.Queue):
    snmpEngine = SnmpEngine()

    iterator = get_cmd(
        snmpEngine,
        # SNMPv1 = mpModel=0 (SNMPv2c would be mpModel=1)
        # CommunityData("public", mpModel=0),
        USMUSRDATA,
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

    returnDict = {
        "source": "IDRAC",
        "value": returnObj,
        "type": "snmpPyIDRACData"
    }
    # return returnObj
    queueToInsrt.put(returnDict)


# IDRAC get FAN data
async def walk_column_v3(snmpEngine, remoteIP: str, base_oid: str) -> dict:
    rows = {}
    async for errInd, errStat, errIdx, varBinds in walk_cmd(
        snmpEngine,
        # CommunityData("public", mpModel=0),
        USMUSRDATA,
        await UdpTransportTarget.create((remoteIP, SNMPORT)),
        ContextData(),
        ObjectType(ObjectIdentity(base_oid)),
        lexicographicMode=False,
    ):
        if errInd:
            raise RuntimeError(errInd)
        if errStat:
            raise RuntimeError(errStat.prettyPrint())

        for oid, val in varBinds:
            # index is typically the last sub-identifier
            idx = int(oid.prettyPrint().split(".")[-1])
            rows[idx] = val.prettyPrint()

    return rows

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
