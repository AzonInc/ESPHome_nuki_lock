#include "led_enabled_switch.h"

namespace esphome {
namespace nuki_lock {

void NukiLockLedEnabledSwitch::setup() {
    this->publish_state(false);
}

void NukiLockLedEnabledSwitch::dump_config() {
    LOG_SWITCH(TAG, "LED Enabled", this);
}

void NukiLockLedEnabledSwitch::write_state(bool state) {
    this->parent_->set_led_enabled(state);
}

}  // namespace nuki_lock
}  // namespace esphome