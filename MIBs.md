# IDRAC8

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