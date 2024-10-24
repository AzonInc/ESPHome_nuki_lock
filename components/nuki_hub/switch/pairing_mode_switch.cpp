#include "pairing_mode_switch.h"

namespace esphome {
namespace nuki_hub {

void PairingModeSwitch::setup() {
    this->publish_state(false);
}

void PairingModeSwitch::dump_config() {
    LOG_SWITCH(TAG, "Pairing Mode", this);
}

void PairingModeSwitch::write_state(bool state) {
    this->parent_->set_pairing_mode(state);
}

}  // namespace nuki_hub
}  // namespace esphome