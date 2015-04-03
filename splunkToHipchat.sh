#!/bin/bash

# This script should be executed by Splunk when an alert fires.
# It acts as a wrapper and allows us to execute whichever version of Python we want.
#
# The arguments that Splunk passes to the script are as follows:
#
# $0 = Script name
# $1 = Number of events returned
# $2 = Search terms
# $3 = Fully qualified query string
# $4 = Name of saved search
# $5 = Trigger reason (i.e. "The number of events was greater than 1")
# $6 = Browser URL to view the saved search
# $7 = This option has been deprecated and is no longer used
# $8 = File where the results for this search are stored (contains raw results)

SPLUNK_SCRIPTS_LOCATION=/opt/splunk/bin/scripts
PYTHON_HOME=/usr/bin/python2.7

## This is crucial as otherwise the Python script won't find the Splunk Python SDK
unset LD_LIBRARY_PATH

SCRIPT_NAME="$0"
NUMBER_OF_EVENTS_RETURNED="$1"
SEARCH_TERMS="$2"
FULLY_QUALIFIED_QUERY_STRING="$3"
NAME_OF_SAVED_SEARCH="$4"
TRIGGER_REASON="$5"
URL="$6"
FILE_ON_DISK="$8"

"$PYTHON_HOME" "$SPLUNK_SCRIPTS_LOCATION"/splunkToHipchat.py "$NAME_OF_SAVED_SEARCH" "$URL" "$SPLUNK_SCRIPTS_LOCATION"