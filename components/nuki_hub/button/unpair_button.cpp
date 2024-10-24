#include "unpair_button.h"

namespace esphome {
namespace nuki_hub {

void UnpairButton::press_action() {
    this->parent_->unpair();
}

void UnpairButton::dump_config() {
    LOG_BUTTON(TAG, "Unpair", this);
}

}  // namespace nuki_hub
}  // namespace esphome