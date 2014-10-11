# Digital Ocean cleaner

Digital Ocean is pretty awesome for many reasons (speed, ssd, cost, etc.). It is very convenient to use their architecture to spawn test boxes.

But it is very easy to spawn test boxes and forget them ... and get billed for it !

This simple script is gonna kill DigitalOcean droplets on your behalf, freeing you from checking if you still have running boxes and let you focus on your work.

# Requirements

Well ... you need Digital Ocean API keys obviously!

# Setup 

```bash
# Install Digital Ocean API library 
pip install dopy

# Install the stuff
pip install .

# Prepare the config file (see below for the format)
vim /etc/do_clean.cfg

# Start the script 
do_clean
```

# Config file

The config file need to be saved, either in `~/.do_clean.cfg`, or `./do_clean.cfg`, or `/etc/do_clean.cfg`

## Format

```
[do_clean]
# Version of the Digital Ocean API - either 1 or 2 (default: 1)
version = 1 

# API credentials
client_id = digitalocean_client_id
api_key = digitalocean_api_key

# Maximum age in sec of a droplet (default: 18000)
max_age = 18000 

# Frequency check of the API in sec (default: 300)
check_freq = 300

# Comma separated list of Droplet to NOT touch
# dont = 12345,54321
```

# TODO

It's a dirty hack but it serves its purpose! 

Many stuff to add to make it great:

- send messages to the logs (file or syslog)
- run as daemon (init script / supervisor...)

I probably won't go through the hassle of doing them unless some people show interest, for now you need to update the script as grown ups.
