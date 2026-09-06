# FoxESS Export Control
### Curtail – Negative Feed In Rates

Home Assistant custom integration for controlling the **FoxESS inverter ExportLimit** through the FoxESS Cloud OpenAPI. No Modbus required.

[![Add FoxESS Export Control to HACS](https://img.shields.io/badge/HACS-Add%20Repository-41BDF5?logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=MrHC1983&repository=FoxESS-Export-Control&category=integration)

## What it does

Creates a writable Home Assistant `number` entity representing the FoxESS `ExportLimit`. Automations can use it for negative-price curtailment, schedules or any other condition. It is deliberately independent of any electricity retailer or price provider.

## Installation

### HACS
Install HACS, then **HACS → Integrations → ⋮ → Custom repositories**, add `https://github.com/MrHC1983/FoxESS-Export-Control`, select **Integration**, install, restart Home Assistant, then add **FoxESS Export Control** under **Settings → Devices & services**. HACS documents custom repositories here: https://www.hacs.dev/docs/faq/custom_repositories/

### Manual
Copy `custom_components/foxess_export_control` to `/config/custom_components/foxess_export_control/`, restart Home Assistant, then add the integration from **Settings → Devices & services**.

## Setup: the two things you need

The integration asks for **two values only**:

1. **FoxESS API key** — no FoxESS username/password is required.
2. **FoxESS device serial number**.

### API key
Log in to FoxESS Cloud using your normal account. If the current interface does not expose API management, use the classic/v1 interface. Open your profile/user centre → **API Management** → generate a personal API key/private token. Copy it immediately; FoxESS may obscure it after leaving the page. Treat it like a password and never publish it.

### Device serial
Get it from the FoxESS app/web portal, device information, or the inverter/data-logger label. Enter it exactly as shown by FoxESS.

## Example

See `examples/negative_feed_in_curtailment.yaml` for a generic negative feed-in automation. Replace the price sensor and export values with your own setup.

## Grid compliance — important

**Never use this project to increase your permitted grid export capacity.** The maximum value used by your automation must remain within the limit permitted by your electricity distributor, connection agreement and applicable requirements.

This project is intended to reduce/manage export. It must not be used to defeat distributor-controlled dynamic export systems, emergency backstop functionality, mandatory grid controls, or other regulatory/installer protections.

If you have a dynamic export connection, that control path remains authoritative.

Support development
If QBitTorrent HomeConnect saves you time, voluntary support for ongoing development and maintenance is welcome:

PayPal: https://paypal.me/MrHC1983

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20Development-FFDD00?logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/MrHC1983)

## Privacy

No developer telemetry, analytics or remote data collection. The integration communicates with Home Assistant and FoxESS Cloud only. See `PRIVACY.md`.

## Independence

FoxESS Export Control is an independent open-source project maintained by **MrHC1983**. It is not affiliated with, endorsed by, or supported by FoxESS, FoxESS Cloud, Home Assistant, electricity retailers or electricity distributors.

## License

MIT — see `LICENSE`.
