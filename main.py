#!/usr/bin/env python3
# Meraki API interaction bot

# 2021 Apr 25

# INSTALL
## pip install slack_sdk
## pip install meraki

# CONFIGURATION
## You need to set shell environmetn variables
## export MERAKI_DASHBOARD_API_KEY=<Meraki dashboard API KEY>
## export MERAKI_ORG_ID=<Organization ID1>:<Organization ID2>
## export MERAKI_NET_ID=<Network ID1>:<Network ID2>
## export SLACK_URL=<Slack incoming webhook URL>

# RUN
## ./main.pl

import os
import time, calendar

# https://slack.dev/python-slack-sdk/api-docs/slack_sdk/index.html
from slack_sdk.webhook import WebhookClient

# set Meraki dashboard API token as a shell environment variable 
# export MERAKI_DASHBOARD_API_KEY=<API KEYS>
# https://github.com/meraki/dashboard-api-python
import meraki

### Meraki SDK config variables
# Disable Meraki SDK logging to console
OUTPUT_LOG = False
# Disable Meraki SDK logging to console
PRINT_TO_CONSOLE = False

# Instantiate Meraki dashboard API
dashboard = meraki.DashboardAPI(output_log=OUTPUT_LOG, print_console=PRINT_TO_CONSOLE)

# Slack Webhook URL
slack_url = os.environ.get('SLACK_URL')
webhook = WebhookClient(slack_url)

# Meraki Organization ID
meraki_organizations = []
for x in os.environ.get('MERAKI_ORG_ID').split(':'):
    meraki_organizations.append(x)

# Meraki Network ID
meraki_networks = []
for x in os.environ.get('MERAKI_NET_ID').split(':'):
    meraki_networks.append(x)

### Functions

def simplepostSlack(message):

    response = webhook.send(text=message)

    assert response.status_code == 200
    assert response.body == "ok"

    return

def postSlack(message):

    response = webhook.send(
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Title"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": "*November 12, 2019*",
                        "type": "mrkdwn"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Title2*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "text"
                }
            }
        ]
    )

    assert response.status_code == 200
    assert response.body == "ok"

    return

def getNetworkEvents(net_id,logstarttime):

    log = []

    # Get network event logs
    my_events = dashboard.networks.getNetworkEvents(networkId=net_id)

    # loop for my_events list
    for x in my_events.get('events'):

        if checkTimestamp(x.get('occurredAt'),logstarttime):
            log.append('Occurred at ' + x.get('occurredAt') + '\n')

            # code block
            log.append('```\n')

            # loop for dict
            for key in x:
                if key != 'occurredAt':
                    if isinstance(x.get(key), str):
                        log.append(key + ' : ' + x.get(key) + '\n')

            log.append('```\n')
        else:
            pass

    return log

def getOrganizationConfigurationChanges(org_id):

    log = []

    # Get Organization Configuration Changes
    my_changes = dashboard.organizations.getOrganizationConfigurationChanges(organizationId=org_id)

    for x in my_changes:
        #print('Date > ', x['ts'])
        #print(' Admin > ', x['adminName'])
        #print(' Page > ', x['page'])
        #print(' Label > ', x['label'])
        #print(' oldValue > ', x['oldValue'])
        #print(' newValue > ', x['newValue'])
        log.append({
            'date': x['ts'],
            'admin': x['adminName'], 
            'page': x['page'],
            'label': x['label'],
            'oldvalue': x['oldValue'],
            'newvalue': x['newValue'],
        })

    return log


def getOrganizationNetworks(org_id):

    my_nets = dashboard.organizations.getOrganizationNetworks(organizationId=org_id)
    for x in my_nets:
        print (" Network name: " + x.get('name'))
        print ("  Network ID: " + x.get('id'))

def getOrganizations():

    # Get a list of Organization associated with provided API token
    my_orgs = dashboard.organizations.getOrganizations()

    for x in my_orgs:
        print("Organization ID: " + x.get('id'))
        print(" Name: " + x.get('name'))
        print(" URL: " + x.get('url'))

def getCurrentGmtime():

    t = int(time.time())

    return t

def checkTimestamp(logtime,basetime):

    # convert calendar time to epoch
    logtime_epoch = calendar.timegm(time.strptime(logtime, "%Y-%m-%dT%H:%M:%S.%fZ"))

    # compare time if it's withing 30 minutes
    if basetime < logtime_epoch:
        return True
    else:
        return False

#def convertUnixtimetoCalendartime

### Main

def main():

    # Obtain current unit time - 30 minutes
    logstarttime = getCurrentGmtime() - 1800

    #print (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t)))

    changelogs = []
    eventlogs = []

    text = '----------CHANGE LOGS----------\n'
    # loop for each Organization
    for x in meraki_organizations:

        if x != '':
            # Obtain configuration change logs
            changelogs = getOrganizationConfigurationChanges(x)

            # loop for log lines
            for y in changelogs:
                if checkTimestamp(y.get('date'),logstarttime):
                    for key in y:
                        text += '`' + key + '` : ' + y.get(key) + '\n'

            simplepostSlack(text)
            time.sleep(1)

    text = '----------EVENT LOGS----------\n'
    for x in meraki_networks:
        if x != '':
            eventlogs = getNetworkEvents(x,logstarttime)
            for y in eventlogs:
                text += y

            simplepostSlack(text)
            time.sleep(1)

    return

if __name__ == "__main__":
    main()