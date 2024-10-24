import esphome.codegen as cg
from esphome.components import lock
import esphome.config_validation as cv

from . import CONF_NUKI_LOCK_ID, NukiLockComponent

CONF_SECURITY_PIN = "security_pin"
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_NUKI_LOCK_ID): cv.use_id(NukiLockComponent),
        cv.Optional(CONF_SECURITY_PIN, default=0): cv.uint16_t
    }
).extend(lock.LOCK_SCHEMA)

async def to_code(config):
    nuki_lock_component = await cg.get_variable(config[CONF_NUKI_LOCK_ID])
    await lock.register_lock(nuki_lock_component, config)
    
    if CONF_SECURITY_PIN in config:
        cg.add(nuki_lock_component.set_security_pin(config[CONF_SECURITY_PIN]))