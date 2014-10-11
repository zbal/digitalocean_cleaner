import os
import sys
from time import mktime, sleep
from datetime import datetime
from dopy.manager import DoManager

import ConfigParser

def load_config_file():
    '''
    Load the config file from either home dir, current folder or global folder
    '''
    p = ConfigParser.ConfigParser()
    path1 = os.path.expanduser(os.environ.get('DO_CLEAN', "~/.do_clean.cfg"))
    path2 = os.getcwd() + "/do_clean.cfg"
    path3 = "/etc/do_clean.cfg"

    if os.path.exists(path1):
        p.read(path1)
    elif os.path.exists(path2):
        p.read(path2)
    elif os.path.exists(path3):
        p.read(path3)
    else:
        return None
    return p

def get_config(p, section, key, env_var, default, integer=False):
    ''' return a configuration variable with casting '''
    value = _get_config(p, section, key, env_var, default)
    if integer:
        return int(value)
    return value


def _get_config(p, section, key, env_var, default):
    ''' helper function for get_config '''
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    if p is not None:
        try:
            return p.get(section, key)
        except:
            return default
    return default

config = load_config_file()
if not config:
    print "Missing config file"
    print "Refer to https://github.com/zbal/digitalocean_cleaner for details about the format"
    sys.exit(1)

# Set details about DO config
client_id = get_config(config, 'do_clean', 'client_id', 'DO_CLIENT_ID', None)
api_key = get_config(config, 'do_clean', 'api_key', 'DO_API_KEY', None)
api_version = get_config(config, 'do_clean', 'version', None, 1, integer=True)

# Set times
# MAX_AGE in seconds of a VM
MAX_AGE = get_config(config, 'do_clean', 'max_age', None, 10800, integer=True)
# CHECK_FREQ in seconds of the DO VM status
CHECK_FREQ = get_config(config, 'do_clean', 'check_freq', None, 300, integer=True)

# DONT touch those Droplets (use droplet ids). ex.
# DONT = [ 123456, 654321 ]
RAW_DONT = get_config(config, 'do_clean', 'dont', None, '')
try:
    DONT = [ int(val.strip()) for val in RAW_DONT.split(',') if val]
except Exception as e:
    print "Invalid format for DONT - %s" % e
    sys.exit(1)

if __name__ == '__main__':
  do = DoManager(client_id, api_key, api_version=api_version)
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
