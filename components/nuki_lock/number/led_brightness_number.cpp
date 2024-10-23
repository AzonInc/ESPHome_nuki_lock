#include "led_brightness_number.h"

namespace esphome {
namespace nuki_lock {

void NukiLockLedBrightnessNumber::setup() {
    this->publish_state(0);
}

void NukiLockLedBrightnessNumber::dump_config() {
    LOG_NUMBER(TAG, "LED Brightness", this);
}

void NukiLockLedBrightnessNumber::control(float value) {
    this->parent_->set_led_brightness(value);
}

}  // namespace nuki_lock
}  // namespace esphome