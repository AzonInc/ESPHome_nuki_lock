#pragma once

#include "esphome/components/switch/switch.h"
#include "../nuki_hub.h"

namespace esphome {
namespace nuki_hub {

class PairingModeSwitch : public switch_::Switch, public Parented<NukiHubComponent> {
   public:
      PairingModeSwitch() = default;
      Trigger<> *get_turn_on_trigger() const;
      Trigger<> *get_turn_off_trigger() const;

   protected:
      void setup() override;
      void dump_config() override;
      void write_state(bool state) override;
      Trigger<> *turn_on_trigger_;
      Trigger<> *turn_off_trigger_;
};

}  // namespace nuki_hub
}  // namespace esphome