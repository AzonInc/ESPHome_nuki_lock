#include "unpair_button.h"

namespace esphome {
namespace nuki_lock {

void NukiLockUnpairButton::press_action() {
    this->parent_->unpair();
}

void NukiLockUnpairButton::dump_config() {
    LOG_BUTTON(TAG, "Unpair", this);
}

}  // namespace nuki_lock
}  // namespace esphome