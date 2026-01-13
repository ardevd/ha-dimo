"""Constants for the DIMO integration."""

from homeassistant.const import UnitOfPower


from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
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
CONF_POLL_INTERVAL = "poll_interval"
DEFAULT_POLL_INTERVAL = 30

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
    state_class: SensorStateClass | None = None
    suggested_display_precision: int | None = None


@dataclass
class DimoSensorDef(SignalDef):
    """Class to hold sensor definition for non vehicle sensors."""

    value_fn: str | Callable | None = None


DIMO_SENSORS: dict[str, DimoSensorDef] = {
    "total_vehicles": DimoSensorDef(
        "Total Dimo Vehicles",
        Platform.SENSOR,
        value_fn="get_total_dimo_vehicles",
        state_class=SensorStateClass.MEASUREMENT,
    )
}

SIGNALS: dict[str, SignalDef] = {
    "dimoAftermarketNSAT": SignalDef("No of GPS Satellites", Platform.SENSOR),
    "lowVoltageBatteryCurrentVoltage": SignalDef(
        "LV Battery Current Voltage",
        Platform.SENSOR,
        SensorDeviceClass.VOLTAGE,
        UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    "isIgnitionOn": SignalDef(
        "Ignition",
        Platform.BINARY_SENSOR,
        BinarySensorDeviceClass.POWER,
    ),
    "speed": SignalDef(
        "Speed",
        Platform.SENSOR,
        SensorDeviceClass.SPEED,
        UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    "powertrainRange": SignalDef(
        "Powertrain Range",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    "powertrainTractionBatteryRange": SignalDef(
        "EV Range",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTransmissionTravelledDistance": SignalDef(
        "Odometer",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
        SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
    ),
    "powertrainTransmissionTemperature": SignalDef(
        "Transmission Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "exteriorAirTemperature": SignalDef(
        "Exterior Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryStateOfChargeCurrent": SignalDef(
        "EV Battery State of Charge",
        Platform.SENSOR,
        SensorDeviceClass.BATTERY,
        PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "chassisAxleRow1WheelLeftTirePressure": SignalDef(
        "Axle Row 1 Wheel Left Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "chassisAxleRow1WheelRightTirePressure": SignalDef(
        "Axle Row 1 Wheel Right Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "chassisAxleRow2WheelLeftTirePressure": SignalDef(
        "Axle Row 2 Wheel Left Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "chassisAxleRow2WheelRightTirePressure": SignalDef(
        "Axle Row 2 Wheel Right Tire Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdBarometricPressure": SignalDef(
        "Barometric Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineSpeed": SignalDef(
        "Engine Speed",
        Platform.SENSOR,
        None,
        REVOLUTIONS_PER_MINUTE,
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineTPS": SignalDef(
        "Throttle Position",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainFuelSystemRelativeLevel": SignalDef(
        "Fuel Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainFuelSystemAbsoluteLevel": SignalDef(
        "Absolute Fuel Level",
        Platform.SENSOR,
        SensorDeviceClass.VOLUME_STORAGE,
        UnitOfVolume.LITERS,
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineDieselExhaustFluidLevel": SignalDef(
        "Diesel Exhaust Fluid Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdIntakeTemp": SignalDef(
        "Intake Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdIsPluggedIn": SignalDef(
        "OBD Plugged in",
        Platform.BINARY_SENSOR,
        BinarySensorDeviceClass.PLUG,
    ),
    "obdEngineLoad": SignalDef(
        "Engine Load",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdStatusDTCCount": SignalDef(
        "Diagnostics Trouble Codes Count",
        Platform.SENSOR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdDTCList": SignalDef(
        "Diagnostics Trouble Codes",
        Platform.SENSOR,
    ),
    "powertrainTractionBatteryChargingIsCharging": SignalDef(
        "EV Battery Charging",
        Platform.BINARY_SENSOR,
        BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    "obdMAP": SignalDef(
        "Intake Manifold Pressure",
        Platform.SENSOR,
        SensorDeviceClass.PRESSURE,
        UnitOfPressure.KPA,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineMAF": SignalDef(
        "Engine Mass Airflow",
        Platform.SENSOR,
        None,
        "g/s",
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryTemperatureAverage": SignalDef(
        "EV Battery Average Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryTemperature": SignalDef(
        "EV Battery Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "currentLocationAltitude": SignalDef(
        "Altitude",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.METERS,
        SensorStateClass.MEASUREMENT,
    ),
    "currentLocationHeading": SignalDef(
        "Heading",
        Platform.SENSOR,
        None,
        DEGREE,
    ),
    "powertrainTractionBatteryGrossCapacity": SignalDef(
        "EV Battery Gross Capacity",
        Platform.SENSOR,
        None,
        UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdRunTime": SignalDef(
        "Engine Run Time",
        Platform.SENSOR,
        None,
        UnitOfTime.SECONDS,
        SensorStateClass.MEASUREMENT,
    ),
    "obdDistanceWithMIL": SignalDef(
        "Distance with MIL",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineECT": SignalDef(
        "Engine Coolant Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "tokenRewards": SignalDef(
        "Total Rewards",
        Platform.SENSOR,
        None,
        "$DIMO",
        SensorStateClass.TOTAL_INCREASING,
    ),
    "powertrainType": SignalDef(
        "Powertrain",
        Platform.SENSOR,
    ),
    "cabinDoorRow1DriverSideWindowIsOpen": SignalDef(
        "Front Driver Side Window Open",
        Platform.BINARY_SENSOR,
    ),
    "cabinDoorRow1PassengerSideWindowIsOpen": SignalDef(
        "Front Passenger Side Window Open",
        Platform.BINARY_SENSOR,
    ),
    "cabinDoorRow2DriverSideWindowIsOpen": SignalDef(
        "Back Driver Side Window Open",
        Platform.BINARY_SENSOR,
    ),
    "cabinDoorRow2PassengerSideWindowIsOpen": SignalDef(
        "Back Passenger Side Window Open",
        Platform.BINARY_SENSOR,
    ),
    "currentLocationIsRedacted": SignalDef(
        "Approximate Location",
        Platform.BINARY_SENSOR,
    ),
    "dimoAftermarketHDOP": SignalDef(
        "Horizontal dilution of GPS precision",
        Platform.SENSOR,
    ),
    "powertrainTractionBatteryStateOfHealth": SignalDef(
        "EV Battery State of Health",
        Platform.SENSOR,
        unit_of_measure=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryCurrentVoltage": SignalDef(
        "EV Battery Current Voltage",
        Platform.SENSOR,
        SensorDeviceClass.VOLTAGE,
        UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryChargingAddedEnergy": SignalDef(
        "Charging Added Energy",
        Platform.SENSOR,
        unit_of_measure=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryChargingChargeLimit": SignalDef(
        "Charging Limit",
        Platform.SENSOR,
        unit_of_measure=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryCurrentPower": SignalDef(
        "EV Battery Current Power",
        Platform.SENSOR,
        SensorDeviceClass.POWER,
        UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "currentLocationLatitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
    "currentLocationLongitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
}
