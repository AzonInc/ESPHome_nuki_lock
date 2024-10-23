import esphome.codegen as cg
from esphome.components import text_sensor
import esphome.config_validation as cv
from esphome.const import (
    UNIT_PERCENT,
    DEVICE_CLASS_BATTERY,
)
from .. import CONF_NUKI_LOCK_ID, NukiLock, nuki_lock_ns

CONF_DOOR_SENSOR_STATE = "door_sensor_state"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLock),
    cv.Optional(CONF_DOOR_SENSOR_STATE): text_sensor.text_sensor_schema(),
}

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])

    if door_sensor_state := config.get(CONF_DOOR_SENSOR_STATE):
        sens = await text_sensor.new_text_sensor(door_sensor_state)
        cg.add(nuki_lock_component.set_door_sensor_state(sens))