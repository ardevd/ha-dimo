"""Constants for the DIMO integration."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    PERCENTAGE,
    Platform,
    UnitOfElectricPotential,
    UnitOfSpeed,
    UnitOfLength,
    UnitOfTemperature,
)

DOMAIN = "dimo"
CONF_PRIVATE_KEY = "private_key"
CONF_AUTH_PROVIDER = "auth_provider"
CONF_LICENSE_ID = "license_id"

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


@dataclass
class SignalDef:
    """Class to hold signal entity definition."""

    name: str
    platform: Platform
    device_class: SensorDeviceClass | BinarySensorDeviceClass | None = None
    unit_of_measure: str | None = None
    icon: str | None = None


# TODO: Add complete list from schema
SIGNALS = {
    "dimoAftermarketNSAT": SignalDef("No of GPS Satellites", Platform.SENSOR),
    "lowVoltageBatteryCurrentVoltage": SignalDef(
        "LV Battery Current Voltage",
        Platform.SENSOR,
        SensorDeviceClass.VOLTAGE,
        UnitOfElectricPotential.VOLT,
    ),
    "speed": SignalDef(
        "Speed",
        Platform.SENSOR,
        SensorDeviceClass.SPEED,
        UnitOfSpeed.KILOMETERS_PER_HOUR,
    ),
    "powertrainTransmissionTravelledDistance": SignalDef(
        "Odometer",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
    ),
    "exteriorAirTemperature": SignalDef(
        "Exterior Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
    ),
    "powertrainTractionBatteryStateOfChargeCurrent": SignalDef(
        "EV Battery State of Charge",
        Platform.SENSOR,
        SensorDeviceClass.BATTERY,
        PERCENTAGE,
    ),
}
