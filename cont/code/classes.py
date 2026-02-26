from pydantic import BaseModel
from sqlalchemy import Column, Date, Float, Integer, String, text
from datetime import datetime, timezone, timedelta
from typing import Optional, Annotated
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT, TEXT, TIMESTAMP, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

# -----------

AlchemyBase = declarative_base()

# DATABASE "CLASSESS"--------------------------------------------
def sensorsqldata(table_name: Annotated[str, "Name of the table"]):

    class SensorSQLDataClass(AlchemyBase):
        __table_args__ = {'extend_existing': True}

        __tablename__ = table_name

        id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)
        time_stamp = Column(
            TIMESTAMP,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
        TEMP = Column(TINYINT)
        TEMP = Column(TEXT)
        TEMP = Column(Float)
        TEMP = Column(Float)
        TEMP = Column(Float, nullable=True)
        TEMP = Column(Float, nullable=True)
        TEMP = Column(Float, nullable=True)

    return SensorSQLDataClass


# Custom--------------------------------------------
class snmpValueToHost():
    def __init__(self, 
                    lastV: Annotated[str, "Last value\nNone when initializing"] = None, 
                    remote: Annotated[str, "Needs to be a valid IP address"] = None, 
                    nextV: Annotated[str, "Value to insert next\nNone when initializing"] = None,
                    lasttime: Annotated[float, "Last time since sending data\nSince Epoch, so time.time()"] = None,
                    lastStatus: Annotated[bool, "True if value newest value was inserted\nFalse if data is pending to be sent"] = False
                ):
        self.__lastValue = lastV       # Save last sent value
        self.__remote = remote          # Remote IP address of the SNMP client
        self.__nextValue = nextV       # Next value to send. Maybe will be used
        self.__lastSentStatus = lastStatus # If previously sent new data, set to True.
        self.__lastSentTime = lasttime if lasttime else time.time()    # The time since the Epoch of the last sent data*


    def ___str__(self):
        return self.__lastValue

    def __changeLastSentValue(self, newValue: int) -> bool:
        self.__nextValue == newValue
        self.__lastValue = self.__nextValue
        self.__nextValue == None
        return True

    def __updateLastSentTime(self):
        self.__lastSentTime = time.time()
        return True

    def __updateSentStatus(self):
        if self.__lastSentStatus:
            self.__lastSentStatus = False
            return False
        else:
            self.__lastSentStatus = True
            return True

    def updateStats(self, nextV: Annotated[int, "Value that will be set as the new one"]):
        __changeLastSentValue(nextV)
        __updateLastSentTime()
        ...


# Dataclasses--------------------------------------------

@dataclass
class snmpPyData():
    """Dataclass for snmp data"""
    hostname: str
    powerDrawPSU1: int
    powerDrawPSU2: int
    voltagePSU1: int
    voltagePSU2: int
    inletTemp: float
    exhaustTemp: float
    uptime: int

    