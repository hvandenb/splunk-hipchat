# Splunk to HipChat

#### Version 1.1

This Splunk to Hipchat script is a quick solution to getting Splunk alerts to send to HipChat. 
It's a bit rough round the edges, but I thought I'd share anyway.

## Getting started with Splunk to Hipchat
- Install Python on your Splunk server. Don't be tempted to rely on the version bundled with Splunk as you will struggle
to install the Splunk SDK for Python that is needed for this script.

- Set PYTHON_HOME and SPLUNK_SCRIPTS_LOCATION inside splunkToHipchat.sh. 
SPLUNK_SCRIPTS_LOCATION should be set to the real path of $SPLUNK_HOME/bin/scripts.

- Install the [Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python) libraries.

- Update splunkToHipchat.config with your configuration. You should only need to change the first three sections unless you want to customise the alert colours and notifications.
Default values are offered for some settings but these are probably inappropriate for your configuration.
 
- Place splunkToHipchat.py, splunkToHipchat.sh and splunkToHipchat.config into $SPLUNK_HOME/bin/scripts. Ensure that you have set execute permissions on the shell script. 

- Configure your Splunk alert(s) action to be 'Run a Script' and point them at splunkToHipchat.sh. This acts acts as a wrapper for the Python script to allows you to use your own version of Python. 
 
- Wait for an alert to fire and watch as it appears in HipChat.

## Requirements
Tested with Python 2.7.6 and Splunk Enterprise 6.2.5 on Linux

## Dependencies
The Python script requires the The [Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python)
to be installed.
 
