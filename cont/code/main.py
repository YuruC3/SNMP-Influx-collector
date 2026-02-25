# import pysnmp, sqlalchemy, ipaddress, os, influxdb_client, re, time
# # SQL
# from sqlalchemy import create_engine, exc  # , Column, Integer, String, Numeric
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# # InfluxDB
# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions
import pysnmp, ipaddress, os, re, time
#SNMP
from easysnmp import Session
# QoL
from typing import Annotated


# Program ENV---------------------------------------
HOST_LIST: Final[list] = os.getenv("HOST_LIST")
try:
    RESOLV_ADDR: Final[str] = ipaddress(os.getenv("RESOLV_ADDR", "1.1.1.1"))
except ValueError:
    raise Exception("Malformed DNS IP address.\nExiting...")


# Flightchecks-------------------------------------------
# Helper functions
def check_host_string(input_text: Annotated[str, "Text to check"]):
    pattern = re.compile(r"^[A-Za-z].*$", re.IGNORECASE)
    return pattern.match(input_text)


# Check if some neccesary ENVs are passed
if not USEINFLUX and not USESQL:
    raise Exception("No database selected to store the data")

# if HOST_LIST empty, raise Exception No hosts passed
if not HOST_LIST:
    raise Exception("No hosts passed\nExiting...")

# for host in HOST_LIST check if valid IP and create a list with strings
HOST_LIST_STR = []
for host in HOST_LIST:
    try:
        if not check_host_string(host):            
            ip = str(ipaddress.IPv4Address(host))
            HOST_LIST_STR.append(ip)
    except ValueError:
        raise Exception("Malformed IP address.\nExiting...")

# Checking if DNS IP is a valid one
# Done under "Program ENV" on line ~18






# Code-------------------------------------------

# Create connections for MySQL and InfluxDB

# functions for inserting data into two DBs


# DNS lookup if the user passed a hostname
# if not given a specific IP for DNS server, fallback to 1.1.1.1

# maybe a class?
# store last value and check if it wasn't sent already to the database
