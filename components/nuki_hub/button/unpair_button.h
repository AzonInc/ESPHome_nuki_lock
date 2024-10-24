#pragma once

#include "esphome/components/button/button.h"
#include "../nuki_hub.h"

namespace esphome {
namespace nuki_hub {

class UnpairButton : public button::Button, public Parented<NukiHubComponent> {
    public:
        UnpairButton() = default;

    protected:
        void press_action() override;
        void dump_config() override;
};

}  // namespace nuki_hub
}  // namespace esphome