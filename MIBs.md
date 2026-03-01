# IDRAC7/8

## temperatureProbeReading

.1.3.6.1.4.1.674.10892.5.4.700.20.1.6 (temperatureProbeReading)

.1.3.6.1.4.1.674.10892.5.4.700.20.1.8 (temperatureProbeLocationName)

Here the temperatureProbeReading.1.1 is the inlet temp, temperatureProbeReading.1.2 is the exhaust temp, temperatureProbeReading.1.3 is the CPU1 temp and temperatureProbeReading.1.4 is CPU2 temp.

These are integers and are written like 250, so decimal needs to be moved to the left to get 25.0

## hostname

.1.3.6.1.2.1.1.5.0 (sysName)

Gets the hostname


## Power
.1.3.6.1.4.1.674.10892.5.4.600.12.1.16 (powerSupplyCurrentInputVoltage)

input voltage for PSU(s)

.1.3.6.1.4.1.674.10892.5.4.600.60.1.15 (powerUsageIdlePower)

Divide by 2 to get power usage

### To get per PSU power in watts

Multiply Amperage by Voltage:

.1.3.6.1.4.1.674.10892.5.4.600.30.1.6 (amperageProbeReading)

1.1 is PSU1 and 1.2 is PSU2

Amperage is in hundreds of miliamps. So if amperageProbeReading read 2, it means that PSUx is drawing 0.2 Amps


.1.3.6.1.4.1.674.10892.5.4.600.20.1.6 (voltageProbeReading)

1.31 is PSU1 and 1.32 is PSU2

Here the voltage i given without deicmal point (240000) so decimal point needs to be moved (240.000) or just convert to int (240)



## Fans

.1.3.6.1.4.1.674.10892.5.4.700.12.1.6 (coolingDeviceReading)

Get each fan one by one from .1.1 to .1.XX; Values in RPM

.1.3.6.1.4.1.674.10892.5.4.700.12.1.19 (coolingDeviceFQDD)

Fan names going from 1.1 to 1.XX; Named coolingDeviceFQDD.1.XX

## other

.1.3.6.1.4.1.674.10892.5.4.1100.30.1.23 (processorDeviceBrandName)

Get the CPU name(s)

.1.3.6.1.4.1.674.10892.5.2.5.0 (systemPowerUpTime)

Uptime in seconds



# IDRAC9

Here the power OID is different :(


## Power 

Here are the OIDs for string 

SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.8.1.1 = STRING: "PS1 Current 1"
SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.8.1.2 = STRING: "PS2 Current 2"
SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.8.1.3 = STRING: "System Board Pwr Consumption"

### Current and Watts

and here are OIDs for intigers. They show miliamps*100. So when ...6.1.1 show 2 it means 2/10 so 100mA = 0.1A. 

BUT the last one is the total board power which is in Watts

SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.6.1.1 = INTEGER: 2
SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.6.1.2 = INTEGER: 10
SNMPv2-SMI::enterprises.674.10892.5.4.600.30.1.6.1.3 = INTEGER: 240

### Voltage

Here are OIDs for Voltage. They need to be divided by 1000 to get 236.000 Volts

PSU1 and PSU2

SNMPv2-SMI::enterprises.674.10892.5.4.600.20.1.6.1.33 = INTEGER: 236000
SNMPv2-SMI::enterprises.674.10892.5.4.600.20.1.6.1.34 = INTEGER: 236000

## Temperatures

Here are the strings for the temp readings

SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.8.1.1 = STRING: "CPU1 Temp"
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.8.1.2 = STRING: "CPU2 Temp"
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.8.1.3 = STRING: "System Board Inlet Temp"
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.8.1.4 = STRING: "System Board Exhaust Temp"


These are temperature readings for inlet and exhaust. They need to be divided by 10 so that 260/10 = 26 C

SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.6.1.1 = INTEGER: 550
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.6.1.2 = INTEGER: 560
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.6.1.3 = INTEGER: 260
SNMPv2-SMI::enterprises.674.10892.5.4.700.20.1.6.1.4 = INTEGER: 310



# NXOS 9.3


## Temperature 

1.3.6.1.4.1.9.9.91.1.1.1.1.4.XXXX (entSensorStatus)

This OID has temperatures 

```
iso.3.6.1.4.1.9.9.91.1.1.1.1.4.38486 = INTEGER: 30
iso.3.6.1.4.1.9.9.91.1.1.1.1.4.38487 = INTEGER: 43
iso.3.6.1.4.1.9.9.91.1.1.1.1.4.38488 = INTEGER: 51
iso.3.6.1.4.1.9.9.91.1.1.1.1.4.38489 = INTEGER: 61
```

### Sensor names

```
iso.3.6.1.2.1.47.1.1.1.1.7.38486 = STRING: "module-1 FRONT"
iso.3.6.1.2.1.47.1.1.1.1.7.38487 = STRING: "module-1 BACK"
iso.3.6.1.2.1.47.1.1.1.1.7.38488 = STRING: "module-1 CPU"
iso.3.6.1.2.1.47.1.1.1.1.7.38489 = STRING: "module-1 Sugarbowl"
```
