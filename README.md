# Digital Ocean cleaner

Digital Ocean is pretty awesome for many reasons (speed, ssd, cost, etc.). It is very convenient to use their architecture to spawn test boxes.

But it is very easy to spawn test boxes and forget them ... and get billed for it !

This simple script is gonna kill DigitalOcean droplets on your behalf, freeing you from checking if you still have running boxes and let you focus on your work.

# Requirements

Well ... you need Digital Ocean API keys obviously!

# Setup 

NOTE: this is not working ! :) don't pip install the thing ... just update the lib/digitalocean_cleaner.py and run it via `python lib/digitalocean_cleaner.py` until fixed

```bash
# Install Digital Ocean API library 
pip install dopy

# Install the stuff
pip install .

# Start the script 
DO_CLIENT_ID='client_id' DO_API_KEY='api_key' do_clean
```

# TODO

It's a dirty hack but it serves its purpose! 

Many stuff to add to make it great:

- config file
- send messages to the logs (file or syslog)
- run as daemon (init script?)

I probably won't go through the hassle of doing them unless some people show interest, for now you need to update the script as grown ups.
