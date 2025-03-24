# Origin
This integration was originally developed through the excellent work of  https://github.com/OStrama/judo_rest_api.git.
The code was heavily modified, extended and adapted to the JUDO ZEWA/PROM iSafe by tach2004.

# judo_rest_api
Home Assistant integration to connect to Judo Zewa/Prom iSafe directly via REST API based on this documentation:

This integration is based on the outstanding work of https://github.com/OStrama/judo_rest_api.git
Thanks to his work that I can also try to integrate the Judo Zewa/Prom iSafe into Homeassistant.

https://judo.eu/app/uploads/2024/11/API-KOMMANDOZEILEN.pdf
Some more basic info can be found here: https://judo.eu/app/downloads/files/de/8203521/manuals/1702574_202405.pdf

Please have a look here to learn more about the communication module that provides the REST API:

https://judo.eu/produkte/connectivity-modul-wlan/

# Judo_rest_api

This integration lets you monitor and control your Judo Zewa/Prom iSafe device locally through it's REST API.
![grafik](https://github.com/user-attachments/assets/00aa6478-ae79-459e-af3e-e2a2ebef6f26)



## Installation

### HACS (manually add Repository)

Add this repository to HACS.
* In the HACS GUI, select "Custom repositories"
* Enter the following repository URL: https://github.com/tach2004/judo_rest_api
* Category: Integration
* Now search in hacs for judo_rest_api, click on it and press the button at the bottom right “download”
* After adding the integration, restart Home Assistant.
* Now press the button "Add Integration" in Configuration -> Integrations to install it in Home assistant.
* Now under Configuration -> Integrations, "Judo REST API" should be available.

### Manual install

Create a directory called `judo_rest_api` in the `<config directory>/custom_components/` directory on your Home Assistant
instance. Install this component by copying all files in `/custom_components/judo_rest_api/` folder from this repo into the
new `<config directory>/custom_components/judo_rest_api/` directory you just created.

This is how your custom_components directory should look like:

```bash
custom_components
├── judo_rest_api
│   ├── __init__.py
│   ├── ...
│   ├── ...
│   ├── ...
│   └── sensor.py  
```
## Configuration
![image](https://github.com/user-attachments/assets/36f25cdd-d969-4b80-bdf8-bdedd86e57ad)


The only mandatory parameters are:
* The IP-Address of your Judo water treatment device. The port should be ok at default (80) unless you changed it in the configuration of the connectivity module.
* The user name. The default value of the connectivity module is "admin". You can change it on the web interface of the connectivity module
* The password. The default value of the connectivity module is "Connectivity". You can change it on the web interface of the connectivity module

The "Device Postfix" has a default value of "". It can be used to add multiple devices to one home assistant. For compatibility this should be left empty. If you want to add another device, use a name that helps to identify the devices.
The "Scan interval" determines how often the REST API is polled. The default value is every 60 seconds. Too small values will cause more timeouts.


# Disclaimer
The developers of this integration are not affiliated with Judo. They have created the integration as open source in their spare time on the basis of publicly accessible information. 
The use of the integration is at the user's own risk and responsibility. The developers are not liable for any damages arising from the use of the integration.

More coming soon to this theater ;-)
