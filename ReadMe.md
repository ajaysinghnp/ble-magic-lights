# BLE Magic Lights - Home Assistant Integration

![BLE Magic Lights](./images/ble-magic-light.png)

**BLE Magic Lights** is a custom Home Assistant integration that allows you to control your BLE-enabled smart lamps. It supports power, static colors, and dynamic effects, using pre-decoded BLE commands.

---

## Features

* **Full control of BLE Magic Lights** via Home Assistant.
* **Power On/Off**, static colors, brightness, and gradient effects.
* **Centralized command database** for easy management and expansion.
* **Manual addition via YAML** or future support for **auto-discovery**.
* Supports **notifications from the lamp** for advanced interactions.
* **Non-intrusive**: unique integration and class names prevent conflicts.

---

## Installation

1. Copy the `ble_magic_lights` folder into your Home Assistant `custom_components/` directory:

```
config/
└── custom_components/
    └── ble_magic_lights/
        ├── __init__.py
        ├── manifest.json
        ├── light.py
        ├── commands.py
        └── config_flow.py   # Optional
```

1. Restart Home Assistant.

---

## Configuration (Manual)

Add the following to your `configuration.yaml`:

```yaml
ble_magic_lights:
  - name: "Living Room Lamp"
    address: "F08083C3-45C3-AB3D-E351-CD1AD4FBDF33"
  - name: "Bedroom Lamp"
    address: "A1B2C3D4-5678-90AB-CDEF-1234567890AB"
```

**Parameters:**

* `name` - Friendly name for the lamp in Home Assistant.
* `address` - Bluetooth MAC address or UUID of the lamp.

---

## Usage

After setup, your BLE Magic Lights will appear as Home Assistant `Light` entities.

### Example Automations

**Turn on lamp with static red color:**

```yaml
service: light.turn_on
target:
  entity_id: light.living_room_lamp
data:
  color_name: "red"
```

**Turn off lamp:**

```yaml
service: light.turn_off
target:
  entity_id: light.living_room_lamp
```

**Set dynamic effect:**

```yaml
service: light.turn_on
target:
  entity_id: light.living_room_lamp
data:
  effect: "seven_color_gradient_high_speed"
```

> Note: Effects and colors are mapped from the command database in `commands.py`.

---

## Commands Database

All pre-decoded BLE commands are stored in `commands.py`. This file includes:

* Power commands (`turn_on`, `turn_off`)
* Static colors (`static_red`, `static_white_low`, `static_blue`, etc.)
* Gradient and dynamic effects (`seven_color_gradient`, `blue_flow_high_speed`, `green_on_red_high_speed`, etc.)

You can **easily add new commands** by updating this file.

---

## Advanced Features

* **Notification handling**: The integration listens to notifications from lamps for feedback.
* **Auto-discovery**: Future versions may support BLE scanning to automatically detect compatible lamps.
* **Custom effects**: Create custom sequences by adding new payloads to the command database.

---

## Requirements

* Home Assistant Core ≥ 2022.12
* Python packages:

  * `bleak` (installed automatically via manifest.json)

---

## Troubleshooting

* Make sure your Home Assistant device has Bluetooth enabled.
* If the lamp is not responding:

  * Check the correct MAC/UUID address.
  * Ensure the lamp is not already connected to another device.
  * Restart Home Assistant.

---

## Contribution

* Fork the repository and submit pull requests.
* Add new command payloads in `commands.py`.
* Report issues on the GitHub repository.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Recommended Future Improvements

* **UI Config Flow**: Add lamps via HA UI without YAML.
* **Full color picker support** for dynamic RGB selection.
* **Auto-discovery** of BLE Magic Lights on the local network.
* **Scheduled effects and automation presets**.

---

### Suggested Integration Name

**`ble_magic_lights`** – unique, descriptive, and avoids collision with other integrations.

---

If you want, I can **also generate a small diagram and table of all commands** for the README, which would make it much easier for users to pick colors/effects quickly.

Do you want me to do that?
