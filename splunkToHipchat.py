import sys
import argparse
import splunklib.client as client
import urllib
import urllib2

if __name__ == "__main__":
    # Parse input params. These come from the wrapper shell script
    parser = argparse.ArgumentParser()
    parser.add_argument('name_of_saved_search')
    parser.add_argument('url')
    parser.add_argument('working_directory')
    args = parser.parse_args()

    # Redirect logs to the same directory as this script lives in
    sys.stdout = open(args.working_directory + '/splunkToHipchat.stdout', 'w')
    sys.stderr = open(args.working_directory + '/splunkToHipchat.stderr', 'w')

    # Configuration
    SPLUNK_HOST = "localhost"
    SPLUNK_PORT = 8089
    SPLUNK_USERNAME = "admin"
    SPLUNK_PASSWORD = "changeme"

    # The delimiter that follows the name of your project at the front of the Splunk alert.
    # E.g. set this to "_" if your alert convention is "PROJECT1_LOW_DISK_SPACE" or set it to " " if
    # your alert is called "Project1 Low Disk Space".
    SPLUNK_ALERT_PREFIX_DELIMITER = " "

    HIPCHAT_BASE_URL = "https://HIPCHAT_URL"
    HIPCHAT_AUTH_TOKEN = "YOUR_AUTH_TOKEN"
    DEFAULT_HIPCHAT_ROOM_NAME = "Splunk alerts with no destination"

    # Splunk alerts map in the following way: Info = 1, Low = 2, Medium = 3, High = 4, Critical = 5
    SPLUNK_SEVERITY_TO_HIPCHAT_COLOUR_DICT = {"1": "green", "2": "green", "3": "yellow", "4": "red", "5": "red"}
    SPLUNK_SEVERITY_TO_HIPCHAT_NOTIFY_DICT = {"1": "false", "2": "false", "3": "true", "4": "true", "5": "true"}
    SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT = {"PROJECT1": "Project alerts 1",
                                                "PROJECT2": "Project alerts 2"}

    splunk_service = client.connect(
        host=SPLUNK_HOST,
        port=SPLUNK_PORT,
        username=SPLUNK_USERNAME,
        password=SPLUNK_PASSWORD)

    def retrieve_splunk_search_results(url, service):
        job_id = url.split('sid=')[1]
        saved_search_as_job = service.jobs[job_id]
        search_results = saved_search_as_job.results(**{"output_mode": "csv"})
        return search_results.read()

    def retrieve_splunk_alert_severity(alert_name, service):
        alert_details = service.saved_searches[alert_name]
        return alert_details["alert.severity"]

    def retrieve_hipchat_room_from_alert_name(alert_name):
        splunk_alert_prefix = alert_name.split(SPLUNK_ALERT_PREFIX_DELIMITER, 1)[0]
        if splunk_alert_prefix in SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT:
            hipchat_room = SPLUNK_ALERT_PREFIX_TO_HIPCHAT_ROOM_DICT[splunk_alert_prefix]
        else:
            hipchat_room = DEFAULT_HIPCHAT_ROOM_NAME
        return hipchat_room

    def send_hipchat_notification(room_id, message, notify, colour):
        url = urllib.basejoin(HIPCHAT_BASE_URL,
                              "/v2/room/" + room_id + "/notification?auth_token=" + HIPCHAT_AUTH_TOKEN)
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