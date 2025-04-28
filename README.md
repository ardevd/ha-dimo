[![Coverage](https://sonarqube.redbird.no/api/project_badges/measure?project=ha-dimo&metric=coverage&token=sqb_643a3d992a975c231854c306cf2a3cdcb1a66f53)](https://sonarqube.redbird.no/dashboard?id=ha-dimo)
[![Lines of Code](https://sonarqube.redbird.no/api/project_badges/measure?project=ha-dimo&metric=ncloc&token=sqb_643a3d992a975c231854c306cf2a3cdcb1a66f53)](https://sonarqube.redbird.no/dashboard?id=ha-dimo)
[![Maintainability Rating](https://sonarqube.redbird.no/api/project_badges/measure?project=ha-dimo&metric=software_quality_maintainability_rating&token=sqb_643a3d992a975c231854c306cf2a3cdcb1a66f53)](https://sonarqube.redbird.no/dashboard?id=ha-dimo)
[![Reliability Rating](https://sonarqube.redbird.no/api/project_badges/measure?project=ha-dimo&metric=software_quality_reliability_rating&token=sqb_643a3d992a975c231854c306cf2a3cdcb1a66f53)](https://sonarqube.redbird.no/dashboard?id=ha-dimo)
[![Security Rating](https://sonarqube.redbird.no/api/project_badges/measure?project=ha-dimo&metric=software_quality_security_rating&token=sqb_643a3d992a975c231854c306cf2a3cdcb1a66f53)](https://sonarqube.redbird.no/dashboard?id=ha-dimo)

# 🚗🔌 DIMO Integration for Home Assistant

Welcome to the **DIMO Integration for Home Assistant**! Bring your vehicle's telemetry data right into Home Assistant. Buckle up, because we're about to take a data-driven joyride!

## 🧐 What's DIMO?

[DIMO](https://dimo.co) is an open-source platform that connects your vehicle to a decentralized network. DIMO provides an open protocol using blockchain to establish universal digital vehicle identity, permissions, data transmission and vehicle control.

## 🚀 Features

- **Sensor Data Galore**: Access a plethora of sensor data for a wide range of supported vehicles via the DIMO telemetry API.

- **Device Tracker**: Keep tabs on your vehicles with device tracker entities. Perfect for ensuring your car isn't sneaking out past curfew.

- **Secure & Trustless Connection**: Enjoy peace of mind with a blockchain-backed, trustless connection to the DIMO API. Your data stays yours without a need to trust a third party server as all data sharing can be validated through smart contract code and transactions all openly available on the blockchain.

## 🛠 Installation

### Option 1: HACS (Home Assistant Community Store)

The integration can be easily added through HACS. Ensure you have [HACS](https://hacs.xyz/) installed and simply search and add the DIMO integration.

### Option 2: Manual Installation

1. Download this repository or check out with `git`. 
2. Copy the `dimo` folder into your `config/custom_components/` directory.
3. Restart Home Assistant to and add the new integration.

## 🔧 Setup Guide

Got the integration installed and ready to connect your car? Follow these steps:

### 0. Sign up to DIMO and connect your vehicle(s)
Download the DIMO mobile app to get going. You can use the Smartcar connection and/or DIMO hardware 
to onboard your vehicle(s). Note that the Smartcar connection provides limited data and only updated data around once every 1-2 hours. Tesla have DIMO integration built in to the infotainment so no hardware device is needed or supported.

### 1. Sign Up on the DIMO Developer Console

- Visit [console.dimo.org](https://console.dimo.org).
- Sign up or log in to your account.
- Create a new application. This requires a license to be minted, which is free for personal use. The application name must be globally unique, so if you get any errors, try modifying the application name.
- Once your application is ready, generate a new api key and add a redirect URI (can be anything, doesnt matter)

### 2. Share Your Vehicle

The Home Assistant integration can only access vehicles you've decided to share with your DIMO console application. This can be done through the DIMO mobile app, but it currently does not support all privileges used by this integration. The recommended way to share your vehicle is through a Login With DIMO URL.

Open up the following URL scheme in your browser: `https://login.dimo.org/?clientId=<users-clientId>&redirectUri=<users-redirectUri>&permissionTemplateId=1&entryState=VEHICLE_MANAGER`. Make sure to substitute your client id and redirect URI according to your DIMO console application.

There you can manage your vehicle sharing. After which, you're ready to set up the integration in Home Assistant.

### 3. Configure the Integration in Home Assistant

- In Home Assistant, go to **Configuration** > **Devices & Services**.
- Click on **Add Integration** and search for "DIMO".
- When prompted, enter your `client_id`, `Redirect URI`, and `API Key`.
- Click **Submit** and let the integration work its magic.

## 🎉 You're All Set!

Congratulations! Your vehicles are now connected to Home Assistant. You can now:

- Monitor real-time sensor data like fuel levels, battery status, and more.
- Track your vehicle's location directly from your Home Assistant dashboard.
- Create automations based on vehicle data (flash your lights when your car arrives home, anyone?).

## 📝 Important Notes
- **Units**: The DIMO API operates with metric units. However, you can easily change the unit of measurement in the entity settings from within Home Assistant.
- **Supported Vehicles**: DIMO supports a vast array of vehicles, but the amount of data you get varies based on vehicle type and how you're connecting to it.
- **Need Help?**: If you encounter any issues, feel free to open an issue on the [GitHub repository](https://github.com/ardevd/ha-dimo).

## 🤝 Contributing

Got ideas to make this integration even better? We'd love to hear from you!

- Fork the repository.
- Make your changes.
- Submit a pull request.
- Earn eternal gratitude (and possibly some good karma).

## 📜 License

This project is licensed under the MIT License—because sharing is caring.

## 🚦 Final Thoughts

This integration, as well as DIMO, is still relatively early in development. Things will change and (hopefully) improve with time.

Also, the maintainers of this integration are not officially affiliated with DIMO.
