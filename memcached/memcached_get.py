#!/usr/bin/env python
# Authors: Stanislav Blokhin

import memcache
import sys

# Config
# Either hostname/IP or UNIX socket
memcached_address=['unix:/var/run/memcached/memcached.sock']

# We need at least one argument
if len(sys.argv) < 2:
	print("%s needs an argument" % sys.argv[0])
	sys.exit(1)

mc = memcache.Client(memcached_address, debug=0)
# Index 0 is script name, index 1 is first argument
key = sys.argv[1]
ret = mc.get(key)

# If no memcached response
if ret is None:
	print("Unknown")
	sys.exit(0)

# All went well
print(ret)
sys.exit(0)
