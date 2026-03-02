import sqlalchemy, os, asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Annotated, Final
from dataclasses import asdict
from models.idracModel import snmpPyIDRACData
from models.sqlTable import idracMeasurement

# SQL ENV-------------------------------------------
USESQL: Final[int] = int(os.getenv("USESQL", 0))
if USESQL:
    DBENGINE: Final[str] = os.getenv("DBENGINE", "mysql+asyncmy")
    DBADDR: Final[str] = os.getenv("DBADDR", "127.0.0.1")
    DBUSR: Final[str] = os.getenv("DBUSR", "root")
    DBPWD: Final[str] = os.getenv("DBPWD", "6767")
    DBNAME: Final[str] = os.getenv("DBNAME", "TEMP_SENSR")


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


async def sqlIDRACDataWriter(
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
                    payload = inpDict["value"]  # snmpPyIDRACData
                    row = asdict(payload)

                    await eng.execute(
                        idracMeasurement.insert(),
                        [row]
                    )
                    return 0
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