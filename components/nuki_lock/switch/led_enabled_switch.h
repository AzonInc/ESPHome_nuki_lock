#pragma once

#include "esphome/components/switch/switch.h"
#include "../nuki_lock.h"

namespace esphome {
namespace nuki_lock {

class NukiLockLedEnabledSwitch : public switch_::Switch, public Parented<NukiLockComponent> {
    public:
        NukiLockLedEnabledSwitch() = default;
        Trigger<> *get_turn_on_trigger() const;
        Trigger<> *get_turn_off_trigger() const;

    protected:
        void setup() override;
        void dump_config() override;
        void write_state(bool state) override;
        Trigger<> *turn_on_trigger_;
        Trigger<> *turn_off_trigger_;
};

}  // namespace nuki_lock
}  // namespace esphome