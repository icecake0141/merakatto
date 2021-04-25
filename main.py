#!/usr/bin/env python3
# Meraki API interaction bot

# set Meraki dashboard API token as a shell environment variable 
# export MERAKI_DASHBOARD_API_KEY=<API KEYS>
# https://github.com/meraki/dashboard-api-python
import meraki

# Disable Meraki SDK loggin
OUTPUT_LOG = False
# Instantiate dashboard API
dashboard = meraki.DashboardAPI(output_log=OUTPUT_LOG)

def main():

    # Get a list of Organization associated with provided API token
    my_orgs = dashboard.organizations.getOrganizations()

    for x in my_orgs:
        print("Organization ID: " + x.get('id'))
        print(" Name: " + x.get('name'))
        print(" URL: " + x.get('url'))
        my_networks = dashboard.organizations.getOrganizationNetworks(organizationId=x.get('id'))
        for y in my_networks:
            print (" Network name: " + y.get('name'))
            print ("  Network ID: " + y.get('id'))

    # Get Organization Configuration Changes
    my_changes = dashboard.organizations.getOrganizationConfigurationChanges(organizationId="956103")

    for x in my_changes:
        print('Date > ', x['ts'])
        print(' Admin > ', x['adminName'])
        print(' Page > ', x['page'])
        print(' Label > ', x['label'])
        print(' oldValue > ', x['oldValue'])
        print(' newValue > ', x['newValue'])

    #my_nets = dashboard.organizations.getOrganizationNetworks()
    #my_nets = dashboard.networks.getNetwork()
    #print(my_nets)

if __name__ == "__main__":
    main()