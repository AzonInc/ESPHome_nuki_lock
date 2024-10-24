import esphome.codegen as cg
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import (
    UNIT_PERCENT,
    DEVICE_CLASS_BATTERY,
)
from . import CONF_NUKI_LOCK_ID, NukiLockComponent

DEPENDENCIES = ["nuki_lock"]

CONF_BATTERY_LEVEL = "battery_level"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLockComponent),
    cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
        device_class=DEVICE_CLASS_BATTERY,
        unit_of_measurement=UNIT_PERCENT,
    ),
}

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])

    if battery_level := config.get(CONF_BATTERY_LEVEL):
        sens = await sensor.new_sensor(battery_level)
        cg.add(nuki_lock_component.set_battery_level(sens))