from homeassistant.const import UnitOfPower

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
    UnitOfVolume,
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


DIMO_SENSORS: dict[str, DimoSensorDef] = {
    "total_vehicles": DimoSensorDef(
        "Total Dimo Vehicles",
        Platform.SENSOR,
        icon="mdi:counter",
        value_fn="get_total_dimo_vehicles",
        state_class=SensorStateClass.TOTAL,
    )
}

SIGNALS: dict[str, SignalDef] = {
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
    "powertrainTractionBatteryRange": SignalDef(
        "EV Range",
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
    "powertrainTransmissionTemperature": SignalDef(
        "Transmission Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
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
        icon="mdi:speedometer",
    ),
    "powertrainFuelSystemRelativeLevel": SignalDef(
        "Fuel Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        icon="mdi:gas-station",
    ),
    "powertrainFuelSystemAbsoluteLevel": SignalDef(
        "Absolute Fuel Level",
        Platform.SENSOR,
        SensorDeviceClass.VOLUME,
        UnitOfVolume.LITERS,
        icon="mdi:gas-station",
    ),
    "powertrainCombustionEngineDieselExhaustFluidLevel": SignalDef(
        "Diesel Exhaust Fluid Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        icon="mdi:fuel",
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
    "obdDTCList": SignalDef(
        "Diagnostics Trouble Codes",
        Platform.SENSOR,
        icon="mdi:alert-circle-outline",
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
    "powertrainTractionBatteryTemperature": SignalDef(
        "EV Battery Temperature",
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
        icon="mdi:engine",
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
    "currentLocationIsRedacted": SignalDef(
        "Approximate Location",
        Platform.BINARY_SENSOR,
        icon="mdi:map-marker",
    ),
    "dimoAftermarketHDOP": SignalDef(
        "Horizontal dilution of GPS precision",
        Platform.SENSOR,
        icon="mdi:satellite-variant",
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
    "powertrainTractionBatteryChargingAddedEnergy": SignalDef(
        "Charging Added Energy",
        Platform.SENSOR,
        unit_of_measure=UnitOfEnergy.KILO_WATT_HOUR,
        icon="mdi:lightning-bolt-circle",
    ),
    "powertrainTractionBatteryChargingChargeLimit": SignalDef(
        "Charging Limit",
        Platform.SENSOR,
        unit_of_measure=PERCENTAGE,
        icon="mdi:ev-station",
    ),
    "powertrainTractionBatteryCurrentPower": SignalDef(
        "EV Battery Current Power",
        Platform.SENSOR,
        SensorDeviceClass.POWER,
        UnitOfPower.WATT,
    ),
    # These are not processed but are here to stop being added as a sensor entity
    "currentLocationLatitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
    "currentLocationLongitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
}
