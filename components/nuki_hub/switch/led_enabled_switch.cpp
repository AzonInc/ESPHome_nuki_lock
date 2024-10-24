#include "led_enabled_switch.h"

namespace esphome {
namespace nuki_hub {

void LedEnabledSwitch::setup() {
    this->publish_state(false);
}

void LedEnabledSwitch::dump_config() {
    LOG_SWITCH(TAG, "LED Enabled", this);
}

void LedEnabledSwitch::write_state(bool state) {
    this->parent_->set_led_enabled(state);
}

}  // namespace nuki_hub
}  // namespace esphome