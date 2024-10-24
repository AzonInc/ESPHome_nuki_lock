#include "button_enabled_switch.h"

namespace esphome {
namespace nuki_hub {

void ButtonEnabledSwitch::setup() {
    this->publish_state(false);
}

void ButtonEnabledSwitch::dump_config() {
    LOG_SWITCH(TAG, "Button Enabled", this);
}

void ButtonEnabledSwitch::write_state(bool state) {
    this->parent_->set_button_enabled(state);
}

}  // namespace nuki_hub
}  // namespace esphome