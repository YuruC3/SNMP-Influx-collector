from pydantic import BaseModel
from sqlalchemy import Column, Date, Float, Integer, String, text
from datetime import datetime, timezone, timedelta
from typing import Optional, Annotated, Dict
from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT, TEXT, TIMESTAMP, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

# -----------

AlchemyBase = declarative_base()

# DATABASE "CLASSESS"--------------------------------------------
# class idracSQLTable(AlchemyBase):
#     def __init__(self, inputData: snmpPyIDRACData):
#         __table_args__ = {'extend_existing': True}

#         __tablename__ = table_name

#         id = Column(MEDIUMINT(unsigned=True), primary_key=True, autoincrement=True)
#         time_stamp = Column(
#             TIMESTAMP,
#             server_default=text("CURRENT_TIMESTAMP"),
#             server_onupdate=text("CURRENT_TIMESTAMP"),
#             nullable=False,
#         )
        
#         inputData.hostname      = Column(TEXT)
#         inputData.powerDrawPSU1 = Column(Float)
#         inputData.powerDrawPSU2 = Column(Float, nullable=True)
#         inputData.voltagePSU1   = Column(Float)
#         inputData.voltagePSU2   = Column(Float, nullable=True)
#         inputData.inletTemp     = Column(Float)
#         inputData.exhaustTemp   = Column(Float)
#         inputData.cpu1Temp      = Column(Float)
#         inputData.cpu2Temp      = Column(Float, nullable=True)
#         inputData.uptimeH       = Column(Float)
#         inputData.uptimeD       = Column(Float, nullable=True)


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
class snmpPyIDRACData():
    """Dataclass for snmp data"""
    hostname: str
    powerDrawPSU1: int
    voltagePSU1: int
    inletTemp: float
    exhaustTemp: float
    cpu1Temp: float
    uptimeH: float

    # optional fields
    uptimeD: float | None = None
    cpu2Temp: float | None = None
    powerDrawPSU2: int | None = None
    voltagePSU2: int | None = None


    def __str__(self):
        return (
            f"{self.hostname}\n"
            f"PSU1 {self.powerDrawPSU1} Watts\n"
            f"PSU2 {self.powerDrawPSU2} Watts\n"
            f"PSU1 {self.voltagePSU1} Volts\n"
            f"PSU2 {self.voltagePSU2} Volts\n"
            f"Inlet {self.inletTemp} C\n"
            f"Exhaust {self.exhaustTemp} C\n"
            f"CPU1 {self.cpu1Temp} C\n"
            f"CPU2 {self.cpu2Temp} C\n"
            f"Uptime {self.uptimeH} Hours\n"
            f"Uptime {self.uptimeD} Days"
            )

@dataclass
class snmpPyCiscoData():
    """Dataclass for snmp data"""
    hostname: str
    powerDrawPSU1: int
    voltagePSU1: int
    inletTemp: float
    exhaustTemp: float
    cpu1Temp: float
    uptimeH: float

    # optional fields
    uptimeD: float | None = None
    cpu2Temp: float | None = None
    powerDrawPSU2: int | None = None
    voltagePSU2: int | None = None


    def __str__(self):
        return (
            f"{self.hostname}\n"
            f"PSU1 {self.powerDrawPSU1} Watts\n"
            f"PSU2 {self.powerDrawPSU2} Watts\n"
            f"PSU1 {self.voltagePSU1} Volts\n"
            f"PSU2 {self.voltagePSU2} Volts\n"
            f"Inlet {self.inletTemp} C\n"
            f"Exhaust {self.exhaustTemp} C\n"
            f"CPU1 {self.cpu1Temp} C\n"
            f"CPU2 {self.cpu2Temp} C\n"
            f"Uptime {self.uptimeH} Hours\n"
            f"Uptime {self.uptimeD} Days"
            )
# @dataclass
# class idracFanStatus:
#     fans: Dict[str, int] | None = Dict[None, None] # name/index -> rpm