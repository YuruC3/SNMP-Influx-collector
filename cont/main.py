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
IDRAC_HOST_LIST: Final[list] = os.getenv("IDRAC_HOST_LIST").split(";")
CISCO_HOST_LIST: Final[list] = os.getenv("CISCO_HOST_LIST").split(";")



# Flightchecks-------------------------------------------
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

async def main():

    # Queues for storing states that a database needs to insert
    # idracQueue  = asyncio.Queue()
    # ciscoQueue  = asyncio.Queue()
    # fanQueue    = asyncio.Queue()
    mainQueue(maxsize=225)

    while True:
        tasks = []
        # IDRAC part
        async with asyncio.TaskGroup() as tg:
            for IdracIP in IDRAC_HOST_LIST:
                tasks.append(tg.create_task(idracPoolRemote_v3(IdracIP, mainQueue)))
                # tasks.append(tg.create_task(idracPoolRemoteFAN_v3(IdracIP, mainQueue)))
                
            
            # for CiscoIP in CISCO_HOST_LIST:
            #     tasks.append(tg.create_task(ciscoPoolRemote(CiscoIP, mainQueue)))

        sleep(20)



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


    loop = asyncio.get_event_loop()
    task = loop.create_task(main())





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

