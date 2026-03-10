from types import SimpleNamespace
from homeassistant.const import Platform

from custom_components.dimo.sensor import DimoSensorEntity, DimoVehicleSensorEntity
from custom_components.dimo.const import DIMO_SENSORS, SIGNALS

class MockSensorDef:
    def __init__(self, unit_of_measure=None, platform=Platform.SENSOR, name="mock_name", device_class=None, icon=None, state_class=None):
        self.unit_of_measure = unit_of_measure
        self.platform = platform
        self.name = name
        self.device_class = device_class
        self.icon = icon
        self.state_class = state_class

def test_dimo_sensor_entity_value(dummy_coordinator):
    key = "test_sensor_key"
    dummy_coordinator.dimo_data = {key: "test_value"}
    
    entity = DimoSensorEntity(dummy_coordinator, "domain", key)
    assert entity.native_value == "test_value"

def test_dimo_sensor_entity_value_missing(dummy_coordinator):
    key = "missing_key"
    dummy_coordinator.dimo_data = {}
    
    entity = DimoSensorEntity(dummy_coordinator, "domain", key)
    assert entity.native_value is None

def test_dimo_sensor_entity_unit(dummy_coordinator, monkeypatch):
    key = "test_sensor_key"
    dummy_coordinator.dimo_data = {key: "test_value"}
    monkeypatch.setitem(DIMO_SENSORS, key, MockSensorDef(unit_of_measure="V"))
    
    entity = DimoSensorEntity(dummy_coordinator, "domain", key)
    assert entity.native_unit_of_measurement == "V"

def test_dimo_sensor_entity_unit_missing(dummy_coordinator):
    key = "unknown_key"
    dummy_coordinator.dimo_data = {key: "test_value"}
    
    entity = DimoSensorEntity(dummy_coordinator, "domain", key)
    assert entity.native_unit_of_measurement is None

def test_dimo_vehicle_sensor_entity_value(dummy_coordinator):
    token = "123456"
    key = "speed"
    vehicle = SimpleNamespace(signal_data={key: {"value": 65}})
    dummy_coordinator.vehicle_data = {token: vehicle}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_value == 65

def test_dimo_vehicle_sensor_entity_value_missing_key(dummy_coordinator):
    token = "123456"
    key = "speed"
    vehicle = SimpleNamespace(signal_data={})
    dummy_coordinator.vehicle_data = {token: vehicle}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_value is None

def test_dimo_vehicle_sensor_entity_value_missing_vehicle(dummy_coordinator):
    token = "123456"
    key = "speed"
    dummy_coordinator.vehicle_data = {}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_value is None

def test_dimo_vehicle_sensor_entity_value_none_data(dummy_coordinator):
    token = "123456"
    key = "speed"
    vehicle = SimpleNamespace(signal_data={key: None})
    dummy_coordinator.vehicle_data = {token: vehicle}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_value is None

def test_dimo_vehicle_sensor_entity_unit(dummy_coordinator):
    token = "123456"
    key = "speed"
    vehicle = SimpleNamespace(signal_data={key: {"value": 65}})
    dummy_coordinator.vehicle_data = {token: vehicle}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_unit_of_measurement == SIGNALS[key].unit_of_measure

def test_dimo_vehicle_sensor_entity_unit_missing(dummy_coordinator):
    token = "123456"
    key = "unknown_signal"
    vehicle = SimpleNamespace(signal_data={key: {"value": 65}})
    dummy_coordinator.vehicle_data = {token: vehicle}
    
    entity = DimoVehicleSensorEntity(dummy_coordinator, token, key)
    assert entity.native_unit_of_measurement is None
