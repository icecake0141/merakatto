#!/usr/bin/env python3
# Meraki API interaction bot

# set Meraki dashboard API token as a shell environment variable 
# export MERAKI_DASHBOARD_API_KEY=<API KEYS>
# https://github.com/meraki/dashboard-api-python
import meraki

# Instantiate dashboard API
dashboard = meraki.DashboardAPI()

# Get a list of Organization associated with provided API token
my_orgs = dashboard.organizations.getOrganizations()

for x in my_orgs:
    print("Organization ID: " + x.get('id'))
    print(" Name: " + x.get('name'))
    print(" URL: " + x.get('url'))

#my_nets = dashboard.organizations.getOrganizationNetworks()
#my_nets = dashboard.networks.getNetwork()
#print(my_nets)
