# Helty/Alpac Ventilation Integration (Local AirGuard App proto)
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/matteomanzoni)

**This integration is used to control and get data from Helty/Alpac CMV (Forced ventilations w/ heat exchanger), all models compatible with the "AirGuard" app should be compatible.**

**This integration was created reverse engineering the raw TCP protocol used by the app, YMMV**

The following platform will be installed:

Platform | Description
-- | --
`sensor` | Show info from the unit (indoor/outdoor temp and humidity implemented, CO2 and VOC can be implemented for specific models)
`switch` | Switch ON and OFF panel leds
`climate` | Control of fan speed and presets

## Contributions welcome!

## Helty if you see this, please give me the RFC of protocol :pray:

MIT Licensed
