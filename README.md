# Splunk to HipChat

#### Version 1.0

This Splunk to Hipchat script is a quick solution to getting Splunk alerts to send to HipChat. 
It's a bit rough round the edges, but I thought I'd share anyway.

## Getting started with Splunk to Hipchat
- Configure the settings in splunkToHipchat.py to match your own Splunk and HipChat configuration and login credentials. 
The script requires a v2 authentication token to send alerts to HipChat.

- Install Python on your Splunk server. Don't be tempted to rely on the version bundled with Splunk as you will struggle
to install the Splunk SDK for Python that is needed for this script.

- Set PYTHON_HOME and SPLUNK_SCRIPTS_LOCATION inside splunkToHipchat.sh. 
SPLUNK_SCRIPTS_LOCATION should be set to the real path of $SPLUNK_HOME/bin/scripts.

- Install the [Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python) libraries.

- Work out your Splunk alert naming convention. E.g. "PROJECT1_Low_Disk_Space" or "PROJECT1 Low disk space".

- Update the SPLUNK_ALERT_PREFIX_DELIMITER in splunkToHipchat.py to reflect the character you want to use to calculate 
 the PROJECT1 portion of your Splunk alert. By default everything before the first space will be extracted.
 
- Update the mapping between Splunk alert prefixes and the HipChat room names you want to send alerts to in splunkToHipchat.py.
 
- Place splunkToHipchat.py and splunkToHipchat.sh into $SPLUNK_HOME/bin/scripts.

- Configure your Splunk alert(s) action to be 'Run a Script' and point them at splunkToHipchat.sh. This acts acts as a wrapper 
 for the Python script to allows you to use your own version of Python. 
 
- Wait for an alert to fire and watch as it appears in HipChat.

## Requirements
Tested with Python 2.7.6 and Splunk Enterprise 6.2.2 on Linux

## Dependencies
The Python script requires the The [Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python)
to be installed.
 