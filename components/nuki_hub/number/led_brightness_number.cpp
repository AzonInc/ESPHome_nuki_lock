#include "led_brightness_number.h"

namespace esphome {
namespace nuki_hub {

void LedBrightnessNumber::setup() {
    this->publish_state(0);
}

void LedBrightnessNumber::dump_config() {
    LOG_NUMBER(TAG, "LED Brightness", this);
}

void LedBrightnessNumber::control(float value) {
    this->parent_->set_led_brightness(value);
}

}  // namespace nuki_hub
}  // namespace esphome