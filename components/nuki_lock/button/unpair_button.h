#pragma once

#include "esphome/components/button/button.h"
#include "../nuki_lock.h"

namespace esphome {
namespace nuki_lock {

class NukiLockUnpairButton : public button::Button, public Parented<NukiLockComponent> {
 public:
    NukiLockUnpairButton() = default;

 protected:
    void press_action() override;
    void dump_config() override;
};

}  // namespace nuki_lock
}  // namespace esphome