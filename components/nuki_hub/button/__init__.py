import esphome.codegen as cg
from esphome.components import button
import esphome.config_validation as cv
from esphome.const import (
    ENTITY_CATEGORY_CONFIG,
)
from .. import CONF_NUKI_HUB_ID, NukiHubComponent, nuki_hub_ns

UnpairButton = nuki_hub_ns.class_("UnpairButton", button.Button, cg.Component)

CONF_UNPAIR_BUTTON = "unpair"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_NUKI_HUB_ID): cv.use_id(NukiHubComponent),
    cv.Optional(CONF_UNPAIR_BUTTON): button.button_schema(
        UnpairButton,
        entity_category=ENTITY_CATEGORY_CONFIG,
        icon="mdi:link-off",
    ),
}

async def to_code(config):
    nuki_hub_component = await cg.get_variable(config[CONF_NUKI_HUB_ID])

    if unpair := config.get(CONF_UNPAIR_BUTTON):
        b = await button.new_button(unpair)
        await cg.register_parented(b, config[CONF_NUKI_HUB_ID])
        cg.add(nuki_hub_component.set_unpair_button(b))