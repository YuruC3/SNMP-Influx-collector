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



## other

.1.3.6.1.4.1.674.10892.5.4.1100.30.1.23 (processorDeviceBrandName)

Get the CPU name(s)

