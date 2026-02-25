import influxdb_client, sqlalchemy, random, os
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import create_engine, exc  # , Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import Annotated, Final
from classes import *

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions
# import pymysql

# FluxQL ENV----------------------------------------
USEINFLUX: Final[bool] = os.getenv("USEINFLUX", True)
if USEINFLUX:
    INFLXDBTOKEN: Final[str] = os.getenv("INFLXDBTOKEN", "123" )
    INFLUXBCKT: Final[str] = os.getenv("INFLUXBCKT", "SNMPyth")
    INFLUXORG: Final[str] = os.getenv("INFLUXORG", "staging")
    INFLXDBURL: Final[str] = os.getenv("INFLXDBURL", "http://localhost:8086")
    INFXLUXDB_MEASUEREMENT: Final[str] = os.getenv("INFXLUXDB_MEASUEREMENT", "SNMPyth-containrr")
    INFLX_SEPARATE_POINTS: Final[float] = float(os.getenv("INFLX_SEPARATE_POINTS", 0.1))
# SQL ENV-------------------------------------------
USESQL: Final[bool] = os.getenv("USESQL", False)
if USESQL:
    DBENGINE: Final[str] = os.getenv("DBENGINE", "mysql+pymysql")
    DBADDR: Final[str] = os.getenv("DBADDR", "127.0.0.1")
    DBUSR: Final[str] = os.getenv("DBUSR", "root")
    DBPWD: Final[str] = os.getenv("DBPWD", "6767")
    DBNAME: Final[str] = os.getenv("DBNAME", "TEMP_SENSR")


# DBprepare-------------------------------------------
# INFLUX
if USEINFLUX:
    fluxdb_client = influxdb_client.InfluxDBClient(url=INFLXDBURL, token=INFLXDBTOKEN, org=INFLUXORG)
    write_fluxdb_api = fluxdb_client.write_api(write_options=SYNCHRONOUS)
    query_fluxdb_api = fluxdb_client.query_api()
# SQL
if USESQL:
    engine = create_engine(
        f"{DBENGINE}://{DBUSR}:{DBPWD}@{DBADDR}/{DBNAME}",
        pool_pre_ping=True,         # Check connection liveness before using and if needed, recconect
        pool_recycle=3600           # recycle connections older than N (3600 in this case) seconds
    )
    Session = sessionmaker(bind=engine)



def tempsnsrIntoSQLDB(
    tableInp: Annotated[int, "Name of the table"],
    insertData: Annotated[str, "Data to insert"]
    ) -> int:
    f"""
    Insert {DBNAME} data into MariaDB
    :tableInp: Name of the table
    :return: 0 if succesfull, 1 if rolled back on error, 2 if SQL is not enabled 3 if no such table 
    """

    if not USESQL:
        return 2

    # Check if table exists
    if not sqlalchemy.inspect(engine).has_table(tableInp):
        return 3    

    with Session() as session:

        try:

            data = sensorsqldata(tableInp)
            # print("2")

            if inpayload:
                # print("3")
                session.add(data(
                    data = insertData,
                ))
                # print("4")
                
                session.commit() #Attempt to commit all the records
                # print("good")
                return 0
        except Exception as e:
            print(f"Error {e} when sending to mariadb")
            session.rollback() #Rollback the changes on error
            return 1


def tempsnsrIntoFluxQLDB(
    inpayload: Annotated[SensorPayload, "Payload"]
    ) -> int:

    """
    Insert temperature data into InfluxDB
    :inpayload: Payload
    :return: 0 if succesfull, 1 if general error, 2 if Influx is not enabled
    """
    if not USEINFLUX:
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

    # print(write_fluxdb_api.write(bucket=INFLUXBCKT, org=INFLUXORG, record=inflxdb_Data_To_Send))
    # if write_fluxdb_api.write(bucket=INFLUXBCKT, org=INFLUXORG, record=inflxdb_Data_To_Send) == None:

    if write_fluxdb_api.write(bucket=INFLUXBCKT, org=INFLUXORG, record=inflxdb_Data_To_Send):
        # return {"STATUS": "succesfully inserted to InfluxDB"}
        print("0")
        return 0
    else:
        print("1")
        return 1
