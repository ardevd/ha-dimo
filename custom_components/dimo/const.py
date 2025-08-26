from homeassistant.const import UnitOfPower


"""Constants for the DIMO integration."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    DEGREE,
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
        state_class=SensorStateClass.MEASUREMENT,
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
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "speed": SignalDef(
        "Speed",
        Platform.SENSOR,
        SensorDeviceClass.SPEED,
        UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainRange": SignalDef(
        "Powertrain Range",
        Platform.SENSOR,
        SensorDeviceClass.DISTANCE,
        UnitOfLength.KILOMETERS,
        "mdi:map-marker-distance",
        SensorStateClass.MEASUREMENT,
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
        "mdi:counter",
        SensorStateClass.TOTAL_INCREASING,
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
        "RPM",
        "mdi:engine",
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineTPS": SignalDef(
        "Throttle Position",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        "mdi:speedometer",
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainFuelSystemRelativeLevel": SignalDef(
        "Fuel Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        "mdi:gas-station",
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainFuelSystemAbsoluteLevel": SignalDef(
        "Absolute Fuel Level",
        Platform.SENSOR,
        SensorDeviceClass.VOLUME,
        UnitOfVolume.LITERS,
        "mdi:gas-station",
        SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineDieselExhaustFluidLevel": SignalDef(
        "Diesel Exhaust Fluid Level",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        "mdi:fuel",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdIntakeTemp": SignalDef(
        "Intake Temperature",
        Platform.SENSOR,
        SensorDeviceClass.TEMPERATURE,
        UnitOfTemperature.CELSIUS,
        "mdi:thermometer-lines",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdEngineLoad": SignalDef(
        "Engine Load",
        Platform.SENSOR,
        None,
        PERCENTAGE,
        "mdi:engine",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "obdStatusDTCCount": SignalDef(
        "Diagnostics Trouble Codes Count",
        Platform.SENSOR,
        icon="mdi:alert-circle",
        state_class=SensorStateClass.MEASUREMENT,
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
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainCombustionEngineMAF": SignalDef(
        "Engine Mass Airflow",
        Platform.SENSOR,
        None,
        "g/s",
        "mdi:engine",
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
        "mdi:altimeter",
        SensorStateClass.MEASUREMENT,
    ),
    "currentLocationHeading": SignalDef(
        "Heading",
        Platform.SENSOR,
        None,
        DEGREE,
        "mdi:compass-rose",
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
        "mdi:engine",
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
        "mdi:currency-usd",
        SensorStateClass.TOTAL_INCREASING,
    ),
    "powertrainType": SignalDef(
        "Powertrain",
        Platform.SENSOR,
        icon="mdi:car-cog",
    ),
    "cabinDoorRow1DriverSideWindowIsOpen": SignalDef(
        "Front Driver Side Window Open",
        Platform.BINARY_SENSOR,
        icon="mdi:window-open",
    ),
    "cabinDoorRow1PassengerSideWindowIsOpen": SignalDef(
        "Front Passenger Side Window Open",
        Platform.BINARY_SENSOR,
        icon="mdi:window-open",
    ),
    "cabinDoorRow2DriverSideWindowIsOpen": SignalDef(
        "Back Driver Side Window Open",
        Platform.BINARY_SENSOR,
        icon="mdi:window-open",
    ),
    "cabinDoorRow2PassengerSideWindowIsOpen": SignalDef(
        "Back Passenger Side Window Open",
        Platform.BINARY_SENSOR,
        icon="mdi:window-open",
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
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryChargingChargeLimit": SignalDef(
        "Charging Limit",
        Platform.SENSOR,
        unit_of_measure=PERCENTAGE,
        icon="mdi:ev-station",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "powertrainTractionBatteryCurrentPower": SignalDef(
        "EV Battery Current Power",
        Platform.SENSOR,
        SensorDeviceClass.POWER,
        UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # These are not processed but are here to stop being added as a sensor entity
    "currentLocationLatitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
    "currentLocationLongitude": SignalDef("Current Location", Platform.DEVICE_TRACKER),
}
