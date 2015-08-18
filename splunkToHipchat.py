import sys
import argparse
import splunklib.client as client
import urllib
import urllib2
import json
import ConfigParser
from collections import OrderedDict

if __name__ == "__main__":
    # Parse input params. These come from the wrapper shell script
    parser = argparse.ArgumentParser()
    parser.add_argument('name_of_saved_search')
    parser.add_argument('url')
    parser.add_argument('working_directory')
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.optionxform = str  # Retains case sensitivity from configuration file
    config.readfp(open(args.working_directory + '/splunkToHipchat.config'))

    # Redirect logs to the same directory as this script lives in
    sys.stdout = open(args.working_directory + '/splunkToHipchat.stdout', 'w')
    sys.stderr = open(args.working_directory + '/splunkToHipchat.stderr', 'w')

    # Load configuration into dictionary objects
    SPLUNK_CONFIG_DICT = dict(config.items('Splunk configuration'))
    HIPCHAT_CONFIG_DICT = dict(config.items('HipChat configuration'))
    SPLUNK_SEVERITY_TO_HIPCHAT_COLOUR_DICT = dict(config.items('HipChat alert colour rules'))
    SPLUNK_SEVERITY_TO_HIPCHAT_NOTIFY_DICT = dict(config.items('HipChat alert notification rules'))
    SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT = dict(config.items('Alert name to HipChat room mappings'))

    splunk_service = client.connect(
        host=SPLUNK_CONFIG_DICT.get('host'),
        port=SPLUNK_CONFIG_DICT.get('port'),
        username=SPLUNK_CONFIG_DICT.get('username'),
        password=SPLUNK_CONFIG_DICT.get('password'),
        app=SPLUNK_CONFIG_DICT.get('app'))

    def retrieve_splunk_search_results(url, service):
        job_id = url.split('sid=')[1]
        saved_search_as_job = service.jobs[job_id]
        search_results = saved_search_as_job.results(**{"output_mode": "json"})

        read_search_results = search_results.read()
        return format_splunk_search_results(read_search_results)

    def format_splunk_search_results(json_splunk_search_results):
        json_obj = json.loads(json_splunk_search_results, object_pairs_hook=OrderedDict)
        results_element = json_obj['results']

        results_list = []
        for dictionary in results_element:
            for key, value in dictionary.iteritems():
                results_list.append("\"" + key + ": " + value + "\"")

        return ", ".join(results_list)

    def retrieve_splunk_alert_severity(alert_name, service):
        alert_details = service.saved_searches[alert_name]
        return alert_details["alert.severity"]

    def retrieve_hipchat_room_from_alert_name(alert_name):
        hipchat_room = HIPCHAT_CONFIG_DICT.get('defaultroomname')
        for key in sorted(SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT.iterkeys()):
            if key in alert_name:
                return SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT[key]
        return hipchat_room

    def send_hipchat_notification(room_id, message, notify, colour):
        url = urllib.basejoin(HIPCHAT_CONFIG_DICT.get('baseurl'),
                              "/v2/room/" + room_id + "/notification?auth_token=" + HIPCHAT_CONFIG_DICT.get(
                                  'authtoken'))
        values = {'message': message,
                  'color': colour,
                  'notify': notify}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response.read()

    # Build HipChat message
    hipchat_message_content = args.name_of_saved_search + ": " + retrieve_splunk_search_results(args.url,
                                                                                                splunk_service)
    splunk_alert_severity = retrieve_splunk_alert_severity(args.name_of_saved_search, splunk_service)

    hipchat_alert_colour = SPLUNK_SEVERITY_TO_HIPCHAT_COLOUR_DICT[splunk_alert_severity]

    hipchat_notify = SPLUNK_SEVERITY_TO_HIPCHAT_NOTIFY_DICT[splunk_alert_severity]

    hipchat_room_name = retrieve_hipchat_room_from_alert_name(args.name_of_saved_search)

    # Send HipChat message
    send_hipchat_notification(hipchat_room_name, hipchat_message_content, hipchat_notify, hipchat_alert_colour)