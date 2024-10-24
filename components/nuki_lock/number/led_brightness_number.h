#pragma once

#include "esphome/components/number/number.h"
#include "../nuki_lock.h"

namespace esphome {
namespace nuki_lock {

class NukiLockLedBrightnessNumber : public number::Number, public Parented<NukiLockComponent> {
    public:
        NukiLockLedBrightnessNumber() = default;

    protected:
        void setup() override;
        void dump_config() override;
        void control(float value) override;
};

}  // namespace nuki_lock
}  // namespace esphome