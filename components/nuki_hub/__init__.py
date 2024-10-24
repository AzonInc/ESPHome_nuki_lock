import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.const import (
    CONF_ID, 
    CONF_TRIGGER_ID
)

nuki_hub_ns = cg.esphome_ns.namespace('nuki_hub')
NukiHubComponent = nuki_hub_ns.class_('NukiHubComponent', cg.Component)

PairingModeOnTrigger = nuki_hub_ns.class_("PairingModeOnTrigger", automation.Trigger.template())
PairingModeOffTrigger = nuki_hub_ns.class_("PairingModeOffTrigger", automation.Trigger.template())
PairedTrigger = nuki_hub_ns.class_("PairedTrigger", automation.Trigger.template())

CONF_NUKI_HUB_ID = "nuki_hub_id"

CONF_PAIRING_MODE_TIMEOUT = "pairing_mode_timeout"
CONF_SET_PAIRING_MODE = "pairing_mode"

CONF_ON_PAIRING_MODE_ON = "on_pairing_mode_on_action"
CONF_ON_PAIRING_MODE_OFF = "on_pairing_mode_off_action"
CONF_ON_PAIRED = "on_paired_action"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(NukiHubComponent),
        cv.Optional(CONF_PAIRING_MODE_TIMEOUT, default="300s"): cv.positive_time_period_seconds,
        cv.Optional(CONF_ON_PAIRING_MODE_ON): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(PairingModeOnTrigger),
            }
        ),
        cv.Optional(CONF_ON_PAIRING_MODE_OFF): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(PairingModeOffTrigger),
            }
        ),
        cv.Optional(CONF_ON_PAIRED): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(PairedTrigger),
            }
        ),
    }
)

CONFIG_SCHEMA = cv.All(
    CONFIG_SCHEMA.extend(cv.COMPONENT_SCHEMA).extend(cv.polling_component_schema("500ms"))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    if CONF_PAIRING_MODE_TIMEOUT in config:
        cg.add(var.set_pairing_mode_timeout(config[CONF_PAIRING_MODE_TIMEOUT]))

    for conf in config.get(CONF_ON_PAIRING_MODE_ON, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_PAIRING_MODE_OFF, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_PAIRED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)



# Actions
NukiHubUnpairAction = nuki_hub_ns.class_(
    "NukiHubUnpairAction", automation.Action
)

NUKI_HUB_UNPAIR_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(NukiHubComponent)
    }
)

@automation.register_action(
    "nuki_hub.unpair", NukiHubUnpairAction, NUKI_HUB_UNPAIR_SCHEMA
)

async def nuki_hub_unpair_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)




NukiHubPairingModeAction = nuki_hub_ns.class_(
    "NukiHubPairingModeAction", automation.Action
)

NUKI_HUB_SET_PAIRING_MODE_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(NukiHubComponent),
        cv.Required(CONF_SET_PAIRING_MODE): cv.templatable(cv.boolean)
    }
)

@automation.register_action(
    "nuki_hub.set_pairing_mode", NukiHubPairingModeAction, NUKI_HUB_SET_PAIRING_MODE_SCHEMA
)

async def nuki_hub_set_pairing_mode_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_SET_PAIRING_MODE], args, cg.bool_)
    cg.add(var.set_pairing_mode(template_))
    return var