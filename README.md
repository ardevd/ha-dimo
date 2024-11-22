# 🚗🔌 DIMO Integration for Home Assistant

Welcome to the **DIMO Integration for Home Assistant**! Bring your vehicle's telemetry data right into Home Assistant. Buckle up, because we're about to take a data-driven joyride!

## 🧐 What's DIMO?

[DIMO](https://dimo.co) is an open-source platform that connects your vehicle to a decentralized network, providing secure and trustless access to your car's telemetry data. DIMO provides an open protocol using blockchain to establish universal digital vehicle identity, permissions, data transmission and vehicle control.

## 🚀 Features

- **Sensor Data Galore**: Access a plethora of sensor data for a wide range of supported vehicles via the DIMO telemetry API.

- **Device Tracker**: Keep tabs on your vehicles with device tracker entities. Perfect for ensuring your car isn't sneaking out past curfew.

- **Secure & Trustless Connection**: Enjoy peace of mind with a blockchain-backed, trustless connection to the DIMO API. Your data stays yours without a need to trust a third party server.

## 🛠 Installation

First, a quick note. Onboarding is currently a tad bit convoluted and requires a license fee which, as of current writing, needs to be paid with DIMO or POL tokens.
We realize that this is a high bar to entry, but the DIMO team is working on an update that will wave the fee requirement for personal/open source use. 

### Option 1: HACS (Home Assistant Community Store) (COMING SOON)

1. **Prerequisite**: Ensure you have [HACS](https://hacs.xyz/) installed.
2. Navigate to HACS in your Home Assistant sidebar.
3. Click on the "Integrations" tab.
4. Search for "DIMO" and select it.
5. Click "Install" and follow the prompts.
6. Restart Home Assistant to load the integration.

### Option 2: Manual Installation

1. Download this repository or check out with `git`. 
2. Copy the `dimo` folder into your `config/custom_components/` directory.
3. Restart Home Assistant to and add the new integration.

## 🔧 Setup Guide

Ready to connect your car? Follow these steps:

### 0: Sign up to DIMO and connect your vehicle(s)
Download the DIMO mobile app to get going. You can use the smartcar connection and/or DIMO hardware 
to onboard your vehicle(s).

### 1. Sign Up on the DIMO Developer Console

- Visit [console.dimo.org](https://console.dimo.org).
- Sign up or log in to your account.
- Create a new application. This currently requires a license fee, but will be free for personal use in the near future.
- Once your application is ready, generate a new api key and add a redirect URI (can be anything, doesnt matter)

### 2. Share Your Vehicles in the DIMO Mobile App

The Home Assistant integration can only access vehicles you've decided to share with your DIMO console application. 

- Open the DIMO mobile app on your smartphone.
- Select your vehicle and go to "Vehicle Settings"
- Click "Permission Sharing", tap the "+" sign in the top corner and input the `client_id` address from the DIMO console.
- High-five yourself for being tech-savvy! You've just interacted with a blockchain smart contract!
    - You can use tools such as Polygonscan or tenderly to view your transaction and the source code it intercated with! It's pretty cool!

### 3. Configure the Integration in Home Assistant

- In Home Assistant, go to **Configuration** > **Devices & Services**.
- Click on **Add Integration** and search for "DIMO".
- When prompted, enter your `client_id`, `domain`, and `private key`.
- Click **Submit** and let the integration work its magic.

## 🎉 You're All Set!

Congratulations! Your vehicles are now connected to Home Assistant. You can now:

- Monitor real-time sensor data like fuel levels, battery status, and more.
- Track your vehicle's location directly from your Home Assistant dashboard.
- Create automations based on vehicle data (flash your lights when your car arrives home, anyone?).

## 📝 Important Notes

- **Privacy Matters**: Your connection is secure and trustless, thanks to blockchain technology. Your data is yours alone.
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

This integration, as well as DIMO is still relatively early in development. Things will change and (hopefully) improve with time. 

Also, the maintainers of this integration are not officially affiliated with DIMO.
