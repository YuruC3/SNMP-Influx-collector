import ipaddress, os, re, time, asyncio
# SNMP
from pysnmp.hlapi.v3arch.asyncio import *
# QoL
from typing import Annotated, Final
# functions
from db.collectiveWriter import ALLdbIDRACWriter
# idrac SNMP
from idrac import idrac78, idrac9
# Cisco hosts
# from cisco import lob, nyater

# Program ENV---------------------------------------
try:
    IDRAC78_HOST_LIST: Final[list] = os.getenv("IDRAC78_HOST_LIST", None).split(";")
    IDRAC9_HOST_LIST: Final[list] = os.getenv("IDRAC9_HOST_LIST", None).split(";")
    CISCO_HOST_LIST: Final[list] = os.getenv("CISCO_HOST_LIST", None).split(";")
except:
    raise Exception("No IDRAC hosts variable")

GET_INTERVAL: Final[int] = int(os.getenv("GET_INTERVAL", 60))


# Flightchecks-------------------------------------------
# if HOST_LIST empty, raise Exception No hosts passed
if not IDRAC78_HOST_LIST and not CISCO_HOST_LIST and not IDRAC9_HOST_LIST:
    raise Exception("No hosts passed\nExiting...")
# for host in HOST_LIST check if valid IP and create a list with strings
for idrac78Host in IDRAC78_HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(idrac78Host))
    except ValueError:
        raise Exception(f" IP {ip} for IDRAC7/8 devices is invalid.\nExiting...")
for ciscoHost in CISCO_HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(ciscoHost))
    except ValueError:
        raise Exception(f" IP {ip} for Cisco devices is invalid.\nExiting...")
for idrac9Host in IDRAC9_HOST_LIST:
    try:
        ip = str(ipaddress.IPv4Address(idrac9Host))
    except ValueError:
        raise Exception(f" IP {ip} for IDRAC9 devices is invalid.\nExiting...")

# Done under "Program ENV" on line ~18


# Code-------------------------------------------

async def main():

    # Queues for storing states that a database needs to insert
    # idracQueue  = asyncio.Queue()
    # ciscoQueue  = asyncio.Queue()
    # fanQueue    = asyncio.Queue()
    mainQueue = asyncio.Queue(maxsize=225)
    
    asyncio.create_task(ALLdbIDRACWriter(mainQueue))

    while True:
        
        # IDRAC part
        async with asyncio.TaskGroup() as tg:
            for Idrac78IP in IDRAC78_HOST_LIST:
                tg.create_task(idrac78.idrac7_8PoolRemote_v3(Idrac78IP, mainQueue))
            for Idrac9IP in IDRAC9_HOST_LIST:
                tg.create_task(idrac9.idrac9PoolRemote_v3(Idrac9IP, mainQueue))
            # FANS
            #     tg.create_task(idracPoolRemoteFAN_v3(IdracIP, mainQueue))

            # CISCO devices
            # for CiscoIP in CISCO_HOST_LIST:
            #     tg.create_task(ciscoPoolRemote(CiscoIP, mainQueue))

        await asyncio.sleep(GET_INTERVAL)



    # yes = asyncio.run(idracPoolRemote_v3("192.168.20.7"))
    # fan = asyncio.run(idracPoolRemoteFAN_v3("192.168.20.7"))

    # print("fanThingy")
    # # print(fan)
    # for thing in fan:
    #     print(fan[thing]["name"], fan[thing]["rpm"])
    # for thing in fan:
    #     print(thing)

    # print("for loop")
    # print(yes)

    # print("End of code")

if __name__ == "__main__":
    # qu = asyncio.Queue()
    # asyncio.run(idracPoolRemote_v3("192.168.20.7", qu))
    print("Starting")
    asyncio.run(main())
    
    # loop = asyncio.get_event_loop()
    # task = loop.create_task(main())





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

