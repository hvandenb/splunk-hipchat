# Splunk to HipChat

#### Version 1.0

This Splunk to Hipchat script is a quick solution to getting Splunk alerts to send to HipChat. 
It's a bit rough round the edges, but I thought I'd share anyway.

## Getting started with Splunk to Hipchat
Place splunkToHipchat.py and splunkToHipchat.sh into $SPLUNK_HOME/bin/scripts and configure your Splunk alert action 
to 'Run a Script'. Point your Splunk alert at splunkToHipchat.sh, which acts as a wrapper for the Python script
and allows you to use your own version of Python. Ensure that this version of Python has the 
[Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python) installed.

Configure the splunkToHipchat.py settings to match your own custom server configuration and login credentials.
 
Set up your splunk alerts with a prefix that will determine the routing of your alerts. By default this script will take
everything before the first space in your alert name and look that up in the mapping 

## Requirements
Tested with Python 2.7.6 and Splunk Enterprise 6.2.2 on Linux

## Dependencies
The Python script requires the The [Splunk Software Development Kit for Python](https://github.com/splunk/splunk-sdk-python)
to be installed.
 