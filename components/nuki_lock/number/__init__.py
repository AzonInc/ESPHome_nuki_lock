import esphome.codegen as cg
from esphome.components import number
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
)
from .. import CONF_NUKI_LOCK_ID, NukiLockComponent, nuki_lock_ns

NukiLockLedBrightnessNumber = nuki_lock_ns.class_("NukiLockLedBrightnessNumber", number.Number, cg.Component)

DEPENDENCIES = ["nuki_lock"]

CONF_LED_BRIGHTNESS_NUMBER = "led_brightness"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLockComponent),
    cv.Optional(CONF_LED_BRIGHTNESS_NUMBER): number.number_schema(
        NukiLockLedBrightnessNumber,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:bluetooth-connect",
    ),
}

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])

    if led_brightness := config.get(CONF_LED_BRIGHTNESS_NUMBER):
        n = await number.new_number(
            led_brightness, min_value=0, max_value=5, step=1
        )
        await cg.register_parented(n, config[CONF_NUKI_LOCK_ID])
        cg.add(nuki_lock_component.set_led_brightness_number(n))