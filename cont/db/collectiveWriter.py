import asyncio, os
from typing import Annotated, Final
from db.Influx import fluxIDRACWriter
from db.MariaDB import sqlIDRACDataWriter

USEINFLUX: Final[int] = int(os.getenv("USEINFLUX", 1))
USESQL: Final[int] = int(os.getenv("USESQL", 0))

async def ALLdbIDRACWriter(inputQueue: asyncio.Queue) -> None:
    while True:

        # print(inputQueue)

        qu = await inputQueue.get()

        try:
            if USESQL:
                sqlResult = await sqlIDRACDataWriter(qu)
                match sqlResult:
                    case 1:
                        print("Wrong source")
                    case 2:
                        print("Error inserting to database")
                    case 3:
                        print("No engine defined")
                    case _:
                        print("Inserted in SQL")
            if USEINFLUX:
                fluxResult = await fluxIDRACWriter(qu)
                match fluxResult:
                    case 1:
                        print("could not insert")
                    case 2:
                        print("Error with initializing Inxlux variables")
                    case _:
                        print("Inserted to InfluxDB")
        except Exception as e:
            print(e)
        finally:
            inputQueue.task_done()
