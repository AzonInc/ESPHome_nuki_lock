import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import lock
from esphome.const import (
    CONF_ID, 
    CONF_TRIGGER_ID
)

CONF_NUKI_LOCK_ID = "nuki_lock_id"

CONF_SECURITY_PIN = "security_pin"
CONF_PAIRING_TIMEOUT = "pairing_timeout"

CONF_SET_PAIRING_MODE = "pairing_mode"

CONF_ON_PAIRING_MODE_ON = "on_pairing_mode_on_action"
CONF_ON_PAIRING_MODE_OFF = "on_pairing_mode_off_action"
CONF_ON_PAIRED = "on_paired_action"

nuki_lock_ns = cg.esphome_ns.namespace('nuki_lock')
NukiLockComponent = nuki_lock_ns.class_('NukiLockComponent', lock.Lock, cg.Component)

PairingModeOnTrigger = nuki_lock_ns.class_("PairingModeOnTrigger", automation.Trigger.template())
PairingModeOffTrigger = nuki_lock_ns.class_("PairingModeOffTrigger", automation.Trigger.template())
PairedTrigger = nuki_lock_ns.class_("PairedTrigger", automation.Trigger.template())

CONFIG_SCHEMA = lock.LOCK_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(NukiLockComponent),
    cv.Optional(CONF_PAIRING_TIMEOUT, default="300s"): cv.positive_time_period_seconds,
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
}).extend(cv.polling_component_schema("500ms"))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await lock.register_lock(var, config)
    if CONF_SECURITY_PIN in config:
        cg.add(var.set_security_pin(config[CONF_SECURITY_PIN]))
    
    if CONF_PAIRING_TIMEOUT in config:
        cg.add(var.set_pairing_timeout(config[CONF_PAIRING_TIMEOUT]))

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
NukiLockUnpairAction = nuki_lock_ns.class_(
    "NukiLockUnpairAction", automation.Action
)

NUKI_LOCK_UNPAIR_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(NukiLockComponent)
    }
)

@automation.register_action(
    "nuki_lock.unpair", NukiLockUnpairAction, NUKI_LOCK_UNPAIR_SCHEMA
)

async def nuki_lock_unpair_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)




NukiLockPairingModeAction = nuki_lock_ns.class_(
    "NukiLockPairingModeAction", automation.Action
)

NUKI_LOCK_SET_PAIRING_MODE_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(NukiLockComponent),
        cv.Required(CONF_SET_PAIRING_MODE): cv.templatable(cv.boolean)
    }
)

@automation.register_action(
    "nuki_lock.set_pairing_mode", NukiLockPairingModeAction, NUKI_LOCK_SET_PAIRING_MODE_SCHEMA
)

async def nuki_lock_set_pairing_mode_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_SET_PAIRING_MODE], args, cg.bool_)
    cg.add(var.set_pairing_mode(template_))
    return var