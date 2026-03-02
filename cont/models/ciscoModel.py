from dataclasses import dataclass
from typing import Optional, Annotated, Dict


@dataclass
class snmpPyCiscoData():
    """Dataclass for snmp data"""
    hostname: str
    powerDrawPSU1: int
    voltagePSU1: int
    inletTemp: float
    exhaustTemp: float
    cpu1Temp: float
    uptimeS: int
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
            f"Uptime {self.uptimeS} Seconds\n"
            f"Uptime {self.uptimeH} Hours\n"
            f"Uptime {self.uptimeD} Days"
            )