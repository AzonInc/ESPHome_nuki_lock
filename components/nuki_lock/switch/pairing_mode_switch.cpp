#include "pairing_mode_switch.h"

namespace esphome {
namespace nuki_lock {

void NukiLockPairingModeSwitch::setup() {
    this->publish_state(false);
}

void NukiLockPairingModeSwitch::dump_config() {
    LOG_SWITCH(TAG, "Pairing Mode", this);
}

void NukiLockPairingModeSwitch::write_state(bool state) {
    this->parent_->set_pairing_mode(state);
}

}  // namespace nuki_lock
}  // namespace esphome