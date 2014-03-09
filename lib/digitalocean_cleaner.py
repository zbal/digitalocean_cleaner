import os
from time import mktime, sleep
from datetime import datetime
from dopy.manager import DoManager

# Dirty .. either set your digitalocean API keys here or use ENV
client_id = '' or os.environ.get('DO_CLIENT_ID') 
api_key= '' or os.environ.get('DO_API_KEY')

# MAX_AGE in seconds of a VM
MAX_AGE = 10800 
# CHECK_FREQ in seconds of the DO VM status
CHECK_FREQ = 300

# DONT touch those Droplets (use droplet ids). ex.
# DONT = [ 123456, 654321 ]
DONT = []

if __name__ == '__main__':
  do = DoManager(client_id, api_key)
  while True:
    try:
      droplets = do.all_active_droplets()
      for droplet in droplets:
        if droplet.get('id') in DONT:
          # Don't kill meeeeee
          print 'Not killing %s (%s) - part of the DONT' % (droplet.get('name'), droplet.get('id'))
          continue
        created = datetime.strptime(droplet.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.now()
        diff = now - created
        if diff.seconds > MAX_AGE:
          print 'gonna destroy droplet - %s (%s: %s)' % (droplet.get('name'), droplet.get('id'), droplet.get('ip_address'))
          do.destroy_droplet(droplet.get('id'))
          print 'destroyed droplet - %s (%s: %s)' % (droplet.get('name'), droplet.get('id'), droplet.get('ip_address'))
        else:
          print 'droplet %s (%s: %s) is less than %s sec (age: %s sec)' % (droplet.get('name'), droplet.get('id'), droplet.get('ip_address'), MAX_AGE, diff.seconds)
      print '.'
    except Exception as e:
      # Don't want to crash ! just wait and try again in 5 min
      print 'Error: %s' % (e,)

    # Sleep another 5 min and retry to kill
    sleep(CHECK_FREQ)
