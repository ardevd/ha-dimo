# 🚗🔌 DIMO Integration for Home Assistant

Welcome to the **DIMO Integration for Home Assistant**! Bring your vehicle's telemetry data right into Home Assistant. Buckle up, because we're about to take a data-driven joyride!

## 🧐 What's DIMO?

[DIMO](https://dimo.co) is an open-source platform that connects your vehicle to a decentralized network, providing secure and trustless access to your car's telemetry data. DIMO provides an open protocol using blockchain to establish universal digital vehicle identity, permissions, data transmission and vehicle control.

## 🚀 Features

- **Sensor Data Galore**: Access a plethora of sensor data for a wide range of supported vehicles via the DIMO telemetry API.

- **Device Tracker**: Keep tabs on your vehicles with device tracker entities. Perfect for ensuring your car isn't sneaking out past curfew.

- **Secure & Trustless Connection**: Enjoy peace of mind with a blockchain-backed, trustless connection to the DIMO API. Your data stays yours without a need to trust a third party server.

## 🛠 Installation

### Option 1: HACS (Home Assistant Community Store)

A [PR](https://github.com/hacs/default/pull/2860) exists for including this integration in HACS, but as of now the PR backlog in HACS is almost a year long, so it will probably take some time before it gets merged.

Until then, the integration can be added as a custom repository in HACS for simple integration management.

1. **Prerequisite**: Ensure you have [HACS](https://hacs.xyz/) installed.
2. Navigate to HACS in your Home Assistant sidebar.
3. Click on the three dots in the top right corner. 
4. Select "Custom Repositories"
5. Input "https://github.com/ardevd/ha-dimo" as the repository value, and pick "Integration" as the type.
6. Click "Add"
7. The integration should be installed, and you'll have to restart Home Assistant for the changes to be applied.
8. Finally, add the integration under Settings -> Devices & Services to get started!

### Option 2: Manual Installation

1. Download this repository or check out with `git`. 
2. Copy the `dimo` folder into your `config/custom_components/` directory.
3. Restart Home Assistant to and add the new integration.

## 🔧 Setup Guide

Ready to connect your car? Follow these steps:

### 0. Sign up to DIMO and connect your vehicle(s)
Download the DIMO mobile app to get going. You can use the smartcar connection and/or DIMO hardware 
to onboard your vehicle(s).

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
