#!/usr/bin/env python3
# Meraki API interaction bot

import os

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
for x in os.environ.get('MERAKI_ORG_ID'):
    meraki_organizations.append(x)

# Meraki Network ID
meraki_networks = []
for x in os.environ.get('MERAKI_NET_ID'):
    meraki_networks.append(x)

### Functions

def postSlack(message):

    response = webhook.send(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
                }
            }
        ]
    )

    assert response.status_code == 200
    assert response.body == "ok"

    return

def getOrganizationConfigurationChanges(org_id):

    # Get Organization Configuration Changes
    my_changes = dashboard.organizations.getOrganizationConfigurationChanges(organizationId=org_id)

    for x in my_changes:
        print('Date > ', x['ts'])
        print(' Admin > ', x['adminName'])
        print(' Page > ', x['page'])
        print(' Label > ', x['label'])
        print(' oldValue > ', x['oldValue'])
        print(' newValue > ', x['newValue'])

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

### Main

def main():

    return 0

if __name__ == "__main__":
    main()