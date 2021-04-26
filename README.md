# merakatto

This bot retrieves the latest change / event logs for the last 30 minutes from Meraki dashboard and post it to Slack channel.

# INSTALL

```
pip install slack_sdk
pip install meraki
```

# CONFIGURATION

You need to set shell environment variables.

```
$ export MERAKI_DASHBOARD_API_KEY=<Meraki dashboard API KEY>
$ export MERAKI_ORG_ID=<Organization ID1>:<Organization ID2>
$ export MERAKI_NET_ID=<Network ID1>:<Network ID2>
$ export SLACK_URL=<Slack incoming webhook URL>
```

# RUN
```
$ ./main.pl
```
