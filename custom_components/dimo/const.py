"""Constants for the DIMO integration."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    PERCENTAGE,
    Platform,
    UnitOfElectricPotential,
    UnitOfLength,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)

DOMAIN = "dimo"
CONF_PRIVATE_KEY = "private_key"
CONF_AUTH_PROVIDER = "auth_provider"
CONF_LICENSE_ID = "license_id"

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
]


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
    "powertrainRange": SignalDef(
        "Powertrain Range",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
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
    "chassisAxleRow1WheelLeftTirePressure": SignalDef(
        "Axle Row 1 Wheel Left Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    "chassisAxleRow1WheelRightTirePressure": SignalDef(
        "Axle Row 1 Wheel Right Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    "chassisAxleRow2WheelLeftTirePressure": SignalDef(
        "Axle Row 2 Wheel Left Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    "chassisAxleRow2WheelRightTirePressure": SignalDef(
        "Axle Row 2 Wheel Right Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    "obdBarometricPressure": SignalDef(
        "Barometric Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    # These are not processed but are here to stop being added as a sensor entity
    "currentLocationLatitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
    "currentLocationLongitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
}
