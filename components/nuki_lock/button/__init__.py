import esphome.codegen as cg
from esphome.components import button
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
)
from .. import CONF_NUKI_LOCK_ID, NukiLockComponent, nuki_lock_ns

NukiLockUnpairButton = nuki_lock_ns.class_("NukiLockUnpairButton", button.Button, cg.Component)

DEPENDENCIES = ["nuki_lock"]

CONF_UNPAIR_BUTTON = "unpair"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLockComponent),
    cv.Optional(CONF_UNPAIR_BUTTON): button.button_schema(
        NukiLockUnpairButton,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:link-off",
    ),
}

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])

    if unpair := config.get(CONF_UNPAIR_BUTTON):
        b = await button.new_button(unpair)
        await cg.register_parented(b, config[CONF_NUKI_LOCK_ID])
        cg.add(nuki_lock_component.set_unpair_button(b))