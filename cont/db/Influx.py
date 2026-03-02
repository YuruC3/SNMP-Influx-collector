import influxdb_client, os, asyncio
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions
from typing import Annotated, Final
from models.idracModel import snmpPyIDRACData

# FluxQL ENV----------------------------------------
USEINFLUX: Final[int] = int(os.getenv("USEINFLUX", 1))
if USEINFLUX:
    INFLXDBTOKEN: Final[str] = os.getenv("INFLXDBTOKEN", "123" )
    INFLUXBCKT: Final[str] = os.getenv("INFLUXBCKT", "SNMPyth")
    INFLUXORG: Final[str] = os.getenv("INFLUXORG", "staging")
    INFLXDBURL: Final[str] = os.getenv("INFLXDBURL", "http://localhost:8086")
    INFXLUXDB_MEASUEREMENT: Final[str] = os.getenv("INFXLUXDB_MEASUEREMENT", "SNMPyth-containrr")
    INFLX_SEPARATE_POINTS: Final[float] = float(os.getenv("INFLX_SEPARATE_POINTS", 0.1))

# Prepare-------------------------------------------
# INFLUX
if USEINFLUX:
    fluxdb_client = influxdb_client.InfluxDBClient(url=INFLXDBURL, token=INFLXDBTOKEN, org=INFLUXORG)
    write_fluxdb_api = fluxdb_client.write_api(write_options=ASYNCHRONOUS)
    query_fluxdb_api = fluxdb_client.query_api()
else:
    fluxdb_client = write_fluxdb_api = query_fluxdb_api = None

async def fluxIDRACWriter(
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
    influxdb_client.Point(INFXLUXDB_MEASUEREMENT)
    .tag("SOURCE", inpDict["source"])
    .tag("TYPE", inpDict["type"])
    .tag("HOSTNAME", inpDict["value"].hostname)
    .field("PowerDrawPSU1", inpDict["value"].powerDrawPSU1)
    .field("PowerDrawPSU2", inpDict["value"].powerDrawPSU2)
    .field("TotalBoardPower", inpDict["value"].powerDrawBoard)
    .field("VoltagePSU1", inpDict["value"].voltagePSU1)
    .field("VoltagePSU2", inpDict["value"].voltagePSU2)
    .field("InletTemperature", inpDict["value"].inletTemp)
    .field("ExhaustTemperature", inpDict["value"].exhaustTemp)
    .field("TemperatureCPU1", inpDict["value"].cpu1Temp)
    .field("TemperatureCPU2", inpDict["value"].cpu2Temp)
    .field("UptimeInSeconds", inpDict["value"].uptimeS)
    .field("UptimeInHours", inpDict["value"].uptimeH)
    .field("UptimeInDays", inpDict["value"].uptimeD)
    )

    try:
        write_fluxdb_api.write(bucket=INFLUXBCKT, org=INFLUXORG, record=inflxdb_Data_To_Send)
    except Exception as e:
        print(e)
        return 1

    return 0
    # return {"STATUS": "succesfully inserted to InfluxDB"}