import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import (
    DEVICE_CLASS_SWITCH,
    ENTITY_CATEGORY_CONFIG,
)
from .. import CONF_NUKI_HUB_ID, NukiHubComponent, nuki_hub_ns

PairingModeSwitch = nuki_hub_ns.class_("PairingModeSwitch", switch.Switch, cg.Component)
ButtonEnabledSwitch = nuki_hub_ns.class_("ButtonEnabledSwitch", switch.Switch, cg.Component)
LedEnabledSwitch = nuki_hub_ns.class_("LedEnabledSwitch", switch.Switch, cg.Component)

CONF_PAIRING_MODE_SWITCH = "pairing_mode"
CONF_BUTTON_ENABLED_SWITCH = "button_enabled"
CONF_LED_ENABLED_SWITCH = "led_enabled"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_HUB_ID): cv.use_id(NukiHubComponent),
    cv.Optional(CONF_PAIRING_MODE_SWITCH): switch.switch_schema(
        PairingModeSwitch,
        device_class=DEVICE_CLASS_SWITCH,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:bluetooth-connect",
    ),
    cv.Optional(CONF_BUTTON_ENABLED_SWITCH): switch.switch_schema(
        ButtonEnabledSwitch,
        device_class=DEVICE_CLASS_SWITCH,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:bluetooth-connect",
    ),
    cv.Optional(CONF_LED_ENABLED_SWITCH): switch.switch_schema(
        LedEnabledSwitch,
        device_class=DEVICE_CLASS_SWITCH,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:bluetooth-connect",
    ),
}


async def to_code(config):
    nuki_hub_component = await cg.get_variable(config[CONF_NUKI_HUB_ID])

    if pairing_mode := config.get(CONF_PAIRING_MODE_SWITCH):
        s = await switch.new_switch(pairing_mode)
        await cg.register_parented(s, config[CONF_NUKI_HUB_ID])
        cg.add(nuki_hub_component.set_pairing_mode_switch(s))

    if button_enabled := config.get(CONF_BUTTON_ENABLED_SWITCH):
        s = await switch.new_switch(button_enabled)
        await cg.register_parented(s, config[CONF_NUKI_HUB_ID])
        cg.add(nuki_hub_component.set_button_enabled_switch(s))

    if led_enabled := config.get(CONF_LED_ENABLED_SWITCH):
        s = await switch.new_switch(led_enabled)
        await cg.register_parented(s, config[CONF_NUKI_HUB_ID])
        cg.add(nuki_hub_component.set_led_enabled_switch(s))