#pragma once

#include "esphome/components/number/number.h"
#include "../nuki_hub.h"

namespace esphome {
namespace nuki_hub {

class LedBrightnessNumber : public number::Number, public Parented<NukiLockComponent> {
    public:
        LedBrightnessNumber() = default;

    protected:
        void setup() override;
        void dump_config() override;
        void control(float value) override;
};

}  // namespace nuki_hub
}  // namespace esphome