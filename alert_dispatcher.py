#!/usr/bin/env python

from datetime import datetime
import sys


def handle_alert():
    '''
  # handle_alert method which is called from Ambari
  # :param definitionName: the alert definition unique ID
  # :param definitionLabel: the human readable alert definition label
  # :param serviceName: the service that the alert definition belongs to
  # :param alertState: the state of the alert (OK, WARNING, etc)
  # :param alertText: the text of the alert
  # :param alertTimestamp: the timestamp the alert went off - Added in AMBARI-20291
  # :param hostname: the hostname the alert fired off for - Added in AMBARI-20291
  '''

    definitionName, definitionLabel, serviceName, alertState, alertText, alertTimestamp, hostname = sys.argv[
        1:7]

    # Generate a timestamp for when this script was called
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add custom logic here to handle the alert


if __name__ == '__main__':
    if len(sys.argv) >= 6:
        handle_alert()
    else:
        print("Incorrect number of arguments")
        sys.exit(1)
