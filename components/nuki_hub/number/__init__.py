import esphome.codegen as cg
from esphome.components import number
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
)
from .. import CONF_NUKI_HUB_ID, NukiHubComponent, nuki_hub_ns

LedBrightnessNumber = nuki_hub_ns.class_("LedBrightnessNumber", number.Number, cg.Component)

CONF_LED_BRIGHTNESS_NUMBER = "led_brightness"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_HUB_ID): cv.use_id(NukiHubComponent),
    cv.Optional(CONF_LED_BRIGHTNESS_NUMBER): number.number_schema(
        LedBrightnessNumber,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:bluetooth-connect",
    ),
}

async def to_code(config):
    nuki_hub_component = await cg.get_variable(config[CONF_NUKI_HUB_ID])

    if led_brightness := config.get(CONF_LED_BRIGHTNESS_NUMBER):
        n = await number.new_number(
            led_brightness, min_value=0, max_value=5, step=1
        )
        await cg.register_parented(n, config[CONF_NUKI_HUB_ID])
        cg.add(nuki_hub_component.set_led_brightness_number(n))