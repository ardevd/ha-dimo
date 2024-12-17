"""Constants for the DIMO integration."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    Platform,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
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
    state_class: SensorStateClass | None = None


@dataclass
class DimoSensorDef(SignalDef):
    """Class to hold sensor definition for non vehicle sensors."""

    value_fn: str | Callable | None = None


DIMO_SENSORS = {
    "total_vehicles": DimoSensorDef(
        "Total Dimo Vehicles",
        Platform.SENSOR,
        icon="mdi:counter",
        value_fn="get_total_dimo_vehicles",
        state_class=SensorStateClass.TOTAL,
    )
}

# TODO: Add complete list from schema
SIGNALS = {
    "dimoAftermarketNSAT": SignalDef(
        "No of GPS Satellites", Platform.SENSOR, icon="mdi:satellite-variant"
    ),
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
    "powertrainCombustionEngineSpeed": SignalDef(
        "Engine Speed",
        Platform.SENSOR,
        None,
        "RPM",
        icon="mdi:engine",
    ),
    "powertrainCombustionEngineTPS": SignalDef(
        "Throttle Position",
        Platform.SENSOR,
        None,
        PERCENTAGE,
    ),
    "powertrainFuelSystemRelativeLevel": SignalDef(
        "Fuel Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        icon="mdi:gas-station",
    ),
    "obdIntakeTemp": SignalDef(
        "Intake Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
    ),
    "obdEngineLoad": SignalDef(
        "Engine Load",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        icon="mdi:engine",
    ),
    "powertrainTractionBatteryChargingIsCharging": SignalDef(
        "EV Battery Charging",
        Platform.BINARY_SENSOR,
        BinarySensorDeviceClass.BATTERY_CHARGING,
        None,
    ),
    "obdMAP": SignalDef(
        "Intake Manifold Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
    ),
    "powertrainCombustionEngineMAF": SignalDef(
        "Engine Mass Airflow",
        Platform.SENSOR,
        None,
        "g/s",
        icon="mdi:engine",
    ),
    "powertrainTractionBatteryTemperatureAverage": SignalDef(
        "EV Battery Average Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
    ),
    "currentLocationAltitude": SignalDef(
        "Altitude",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.METERS,
    ),
    "powertrainTractionBatteryGrossCapacity": SignalDef(
        "EV Battery Gross Capacity",
        Platform.SENSOR,
        None,
        UnitOfEnergy.KILO_WATT_HOUR,
    ),
    "obdRunTime": SignalDef(
        "Engine Run Time",
        Platform.SENSOR,
        None,
        UnitOfTime.SECONDS,
    ),
    "obdDistanceWithMIL": SignalDef(
        "Distance with MIL",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
    ),
    "powertrainCombustionEngineECT": SignalDef(
        "Engine Coolant Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
    ),
    "tokenRewards": SignalDef(
        "Total Rewards",
        Platform.SENSOR,
        None,
        "$DIMO",
        icon="mdi:currency-usd",
    ),
    "powertrainType": SignalDef(
        "Powertrain",
        Platform.SENSOR,
        icon="mdi:car-cog",
    ),
    "powertrainTractionBatteryStateOfHealth": SignalDef(
        "EV Battery State of Health",
        Platform.SENSOR,
        unit_of_measure=PERCENTAGE,
        icon="mdi:hospital",
    ),
    "powertrainTractionBatteryCurrentVoltage": SignalDef(
        "EV Battery Current Voltage",
        Platform.SENSOR,
        SensorDeviceClass.VOLTAGE,
        UnitOfElectricPotential.VOLT,
    ),
    # These are not processed but are here to stop being added as a sensor entity
    "currentLocationLatitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
    "currentLocationLongitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
}
