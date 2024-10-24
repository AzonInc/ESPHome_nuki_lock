#include "esphome/core/log.h"
#include "esphome/core/application.h"
#include "nuki_hub.h"

namespace esphome {
namespace nuki_hub {

lock::LockState NukiHubComponent::nuki_to_lock_state(NukiLock::LockState nukiLockState) {
    switch(nukiLockState) {
        case NukiLock::LockState::Locked:
            return lock::LOCK_STATE_LOCKED;
        case NukiLock::LockState::Unlocked:
        case NukiLock::LockState::Unlatched:
            return lock::LOCK_STATE_UNLOCKED;
        case NukiLock::LockState::MotorBlocked:
            return lock::LOCK_STATE_JAMMED;
        case NukiLock::LockState::Locking:
            return lock::LOCK_STATE_LOCKING;
        case NukiLock::LockState::Unlocking:
        case NukiLock::LockState::Unlatching:
            return lock::LOCK_STATE_UNLOCKING;
        default:
            return lock::LOCK_STATE_NONE;
    }
}

bool NukiHubComponent::nuki_doorsensor_to_binary(Nuki::DoorSensorState nukiDoorSensorState) {
    switch(nukiDoorSensorState) {
        case Nuki::DoorSensorState::DoorClosed:
            return false;
        default:
            return true;
    }
}

std::string NukiHubComponent::nuki_doorsensor_to_string(Nuki::DoorSensorState nukiDoorSensorState) {
    switch(nukiDoorSensorState) {
        case Nuki::DoorSensorState::Unavailable:
            return "unavailable";
        case Nuki::DoorSensorState::Deactivated:
            return "deactivated";
        case Nuki::DoorSensorState::DoorClosed:
            return "closed";
        case Nuki::DoorSensorState::DoorOpened:
            return "opened";
        case Nuki::DoorSensorState::DoorStateUnknown:
            return "unknown";
        case Nuki::DoorSensorState::Calibrating:
            return "calibrating";
        default:
            return "undefined";
    }
}

void NukiLockComponent::setup() {
    ESP_LOGI(TAG, "Starting NUKI Lock...");

    // Increase Watchdog Timeout
    // Fixes Pairing Crash
    esp_task_wdt_init(15, false);

    this->scanner_.initialize("ESPHomeNuki");
    this->scanner_.setScanDuration(10);

    this->nukiLock_.registerBleScanner(&this->scanner_);
    this->nukiLock_.initialize();
    this->nukiLock_.setConnectTimeout(BLE_CONNECT_TIMEOUT_SEC);
    this->nukiLock_.setConnectRetries(BLE_CONNECT_TIMEOUT_RETRIES);

    if(this->security_pin_ > 0) {
        bool result = this->nukiLock_.saveSecurityPincode(this->security_pin_);
        if (result) {
            ESP_LOGI(TAG, "Set pincode done");
        } else {
            ESP_LOGE(TAG, "Set pincode failed!");
        }
    }
    
    if (this->nukiLock_.isPairedWithLock()) {
        this->status_update_ = true;
        ESP_LOGI(TAG, "%s Nuki paired", this->deviceName_);
        this->is_paired_->publish_initial_state(true);
    } else {
        ESP_LOGW(TAG, "%s Nuki is not paired", this->deviceName_);
        this->is_paired_->publish_initial_state(false);
    }

    this->publish_state(lock::LOCK_STATE_NONE);

    register_service(&NukiHubComponent::lock_n_go, "lock_n_go");
    register_service(&NukiHubComponent::print_keypad_entries, "print_keypad_entries");
    register_service(&NukiHubComponent::add_keypad_entry, "add_keypad_entry", {"name", "code"});
    register_service(&NukiHubComponent::update_keypad_entry, "update_keypad_entry", {"id", "name", "code", "enabled"});
    register_service(&NukiHubComponent::delete_keypad_entry, "delete_keypad_entry", {"id"});
}

bool NukiLockComponent::valid_keypad_id(int id) {
    bool idValid = std::find(keypadCodeIds_.begin(), keypadCodeIds_.end(), id) != keypadCodeIds_.end();
    if (!idValid) {
        ESP_LOGE(TAG, "keypad id %d unknown.", id);
    }
    return idValid;
}

bool NukiLockComponent::valid_keypad_name(std::string name) {
    bool nameValid = !(name == "" || name == "--");
    if (!nameValid) {
        ESP_LOGE(TAG, "keypad name '%s' is invalid.", name.c_str());
    }
    return nameValid;
}

bool NukiLockComponent::valid_keypad_code(int code) {
    bool codeValid = (code > 100000 && code < 1000000 && (std::to_string(code).find('0') == std::string::npos));
    if (!codeValid) {
        ESP_LOGE(TAG, "keypad code %d is invalid. Code must be 6 digits, without 0.", code);
    }
    return codeValid;
}

void NukiLockComponent::add_keypad_entry(std::string name, int code) {
    if (!keypad_paired_) {
        ESP_LOGE(TAG, "keypad is not paired to Nuki");
        return;
    }

    if (!(valid_keypad_name(name) && valid_keypad_code(code))) {
        ESP_LOGE(TAG, "add_keypad_entry invalid parameters");
        return;
    }

    NukiLock::NewKeypadEntry entry;
    memset(&entry, 0, sizeof(entry));
    size_t nameLen = name.length();
    memcpy(&entry.name, name.c_str(), nameLen > 20 ? 20 : nameLen);
    entry.code = code;
    Nuki::CmdResult result = this->nukiLock_.addKeypadEntry(entry);
    if (result == Nuki::CmdResult::Success) {
        ESP_LOGI(TAG, "add_keypad_entry is sucessful");
    } else {
        ESP_LOGE(TAG, "add_keypad_entry: addKeypadEntry failed (result %d)", result);
    }
}

void NukiLockComponent::update_keypad_entry(int id, std::string name, int code, bool enabled) {
    if (!keypad_paired_) {
        ESP_LOGE(TAG, "keypad is not paired to Nuki");
        return;
    }

    if (!(valid_keypad_id(id) && valid_keypad_name(name) && valid_keypad_code(code))) {
        ESP_LOGE(TAG, "update_keypad_entry invalid parameters");
        return;
    }

    NukiLock::UpdatedKeypadEntry entry;
    memset(&entry, 0, sizeof(entry));
    entry.codeId = id;
    size_t nameLen = name.length();
    memcpy(&entry.name, name.c_str(), nameLen > 20 ? 20 : nameLen);
    entry.code = code;
    entry.enabled = enabled ? 1 : 0;
    Nuki::CmdResult result = this->nukiLock_.updateKeypadEntry(entry);
    if (result == Nuki::CmdResult::Success) {
        ESP_LOGI(TAG, "update_keypad_entry is sucessful");
    } else {
        ESP_LOGE(TAG, "update_keypad_entry: updateKeypadEntry failed (result %d)", result);
    }
}

void NukiLockComponent::delete_keypad_entry(int id) {
    if (!keypad_paired_) {
        ESP_LOGE(TAG, "keypad is not paired to Nuki");
        return;
    }

    if (!valid_keypad_id(id)) {
        ESP_LOGE(TAG, "delete_keypad_entry invalid parameters");
        return;
    }

    Nuki::CmdResult result = this->nukiLock_.deleteKeypadEntry(id);
    if (result == Nuki::CmdResult::Success) {
        ESP_LOGI(TAG, "delete_keypad_entry is sucessful");
    } else {
        ESP_LOGE(TAG, "delete_keypad_entry: deleteKeypadEntry failed (result %d)", result);
    }
}

void NukiLockComponent::print_keypad_entries() {
    if (!keypad_paired_) {
        ESP_LOGE(TAG, "keypad is not paired to Nuki");
        return;
    }

    Nuki::CmdResult result = this->nukiLock_.retrieveKeypadEntries(0, 0xffff);
    if(result == Nuki::CmdResult::Success) {
        ESP_LOGI(TAG, "retrieveKeypadEntries sucess");
        std::list<NukiLock::KeypadEntry> entries;
        this->nukiLock_.getKeypadEntries(&entries);

        entries.sort([](const NukiLock::KeypadEntry& a, const NukiLock::KeypadEntry& b) { return a.codeId < b.codeId; });

        keypadCodeIds_.clear();
        keypadCodeIds_.reserve(entries.size());
        for (const auto& entry : entries) {
            keypadCodeIds_.push_back(entry.codeId);
            ESP_LOGI(TAG, "keypad #%d %s is %s", entry.codeId, entry.name, entry.enabled ? "enabled" : "disabled");
        }
    } else {
        ESP_LOGE(TAG, "print_keypad_entries: retrieveKeypadEntries failed (result %d)", result);
    }
}

void NukiLockComponent::dump_config() {
    
    LOG_LOCK(TAG, "Nuki Lock", this);
    LOG_BINARY_SENSOR(TAG, "Is Connected", this->is_connected_);
    LOG_BINARY_SENSOR(TAG, "Is Paired", this->is_paired_);
    LOG_BINARY_SENSOR(TAG, "Battery Critical", this->battery_critical_);
    LOG_BINARY_SENSOR(TAG, "Door Sensor", this->door_sensor_);
    LOG_TEXT_SENSOR(TAG, "Door Sensor State", this->door_sensor_state_);
    LOG_SENSOR(TAG, "Battery Level", this->battery_level_);
}

void NukiLockComponent::notify(Nuki::EventType eventType) {
    this->status_update_ = true;
    this->config_update_ = true;
    ESP_LOGI(TAG, "event notified %d", eventType);
}

void NukiLockComponent::unpair() {
    if(this->nukiLock_.isPairedWithLock()) {
        this->nukiLock_.unPairNuki();
        ESP_LOGI(TAG, "Unpaired Nuki! Turn on Pairing Mode to pair a new Nuki.");
    } else {
        ESP_LOGE(TAG, "Unpair action called for unpaired Nuki");
    }
}

// Actions
void NukiLockComponent::set_pairing_mode(bool enabled) {
    this->pairing_mode_ = enabled;

    if (this->pairing_mode_switch_ != nullptr)
        this->pairing_mode_switch_->publish_state(enabled);

    if(enabled) {
        ESP_LOGI(TAG, "Pairing Mode turned on for %d seconds", this->pairing_mode_timeout_);
        this->pairing_mode_on_callback_.call();

        ESP_LOGI(TAG, "Waiting for Nuki to enter pairing mode...");

        // Turn on for ... seconds
        uint32_t now_millis = millis();
        this->pairing_mode_timer_ = now_millis + (this->pairing_mode_timeout_ * 1000);
    } else {
        ESP_LOGI(TAG, "Pairing Mode turned off");
        this->pairing_mode_timer_ = 0;
        this->pairing_mode_off_callback_.call();
    }
}

void NukiLockComponent::set_button_enabled(bool enabled) {

    Nuki::CmdResult cmdResult = this->nukiLock_.setButtonEnabled(enabled);

    if (cmdResult == Nuki::CmdResult::Success && this->button_enbutton_switch_ != nullptr) {
        this->button_enabled_switch_->publish_state(enabled);
}

void NukiLockComponent::set_led_enabled(bool enabled) {
    
    Nuki::CmdResult cmdResult = this->nukiLock_.setLedEnabled(enabled);

    if (cmdResult == Nuki::CmdResult::Success && this->led_enabled_switch_ != nullptr) {
        this->led_enabled_switch_->publish_state(enabled);
}

void NukiLockComponent::set_led_brightness(float value) {
    
    Nuki::CmdResult cmdResult = this->nukiLock_.setLedBrightness(static_cast<uint8_t>(value));

    if (cmdResult == Nuki::CmdResult::Success && this->led_brightness_number_ != nullptr) {
        this->led_brightness_number_->publish_state(value);
}

// Callbacks
void NukiHubComponent::add_pairing_mode_on_callback(std::function<void()> &&callback) {
    this->pairing_mode_on_callback_.add(std::move(callback));
}

void NukiHubComponent::add_pairing_mode_off_callback(std::function<void()> &&callback) {
    this->pairing_mode_off_callback_.add(std::move(callback));
}

void NukiHubComponent::add_paired_callback(std::function<void()> &&callback) {
    this->paired_callback_.add(std::move(callback));
}

} //namespace nuki_hub
} //namespace esphome