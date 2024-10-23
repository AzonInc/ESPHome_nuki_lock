import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_DIAGNOSTIC,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_DOOR
)
from .. import CONF_NUKI_LOCK_ID, NukiLockComponent, nuki_lock_ns

DEPENDENCIES = ["nuki_lock"]

CONF_IS_CONNECTED = "is_connected"
CONF_IS_PAIRED = "is_paired"
CONF_BATTERY_CRITICAL = "battery_critical"
CONF_BATTERY_LEVEL = "battery_level"
CONF_DOOR_SENSOR = "door_sensor"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLockComponent),
    cv.Required(CONF_IS_CONNECTED): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_CONNECTIVITY,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Required(CONF_IS_PAIRED): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_CONNECTIVITY,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_BATTERY_CRITICAL): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_BATTERY,
    ),
    cv.Optional(CONF_DOOR_SENSOR): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_DOOR,
    ),
}

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])

    if is_connected := config.get(CONF_IS_CONNECTED):
        sens = await binary_sensor.new_binary_sensor(is_connected)
        cg.add(nuki_lock_component.set_is_connected(sens))

    if is_paired := config.get(CONF_IS_PAIRED):
        sens = await binary_sensor.new_binary_sensor(is_paired)
        cg.add(nuki_lock_component.set_is_paired(sens))

    if battery_critical := config.get(CONF_BATTERY_CRITICAL):
        sens = await binary_sensor.new_binary_sensor(battery_critical)
        cg.add(nuki_lock_component.set_battery_critical(sens))

    if door_sensor := config.get(CONF_DOOR_SENSOR):
        sens = await binary_sensor.new_binary_sensor(door_sensor)
        cg.add(nuki_lock_component.set_door_sensor(sens))