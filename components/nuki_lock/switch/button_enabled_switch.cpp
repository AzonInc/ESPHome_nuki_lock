#include "button_enabled_switch.h"

namespace esphome {
namespace nuki_lock {

void NukiLockButtonEnabledSwitch::setup() {
    this->publish_state(false);
}

void NukiLockButtonEnabledSwitch::dump_config() {
    LOG_SWITCH(TAG, "Button Enabled", this);
}

void NukiLockButtonEnabledSwitch::write_state(bool state) {
    this->parent_->set_button_enabled(state);
}

}  // namespace nuki_lock
}  // namespace esphome