#!/usr/bin/env python
# Authors: Stanislav Blokhin

import memcache

# Config
# Either hostname/IP or UNIX socket
memcached_address=['unix:/var/run/memcached/memcached.sock']

# We need at least one argument
if len(sys.argv) < 2:
	print("usage: %s key" % sys.argv[0])
        sys.exit(1)

# Index 0 is script name, index 1 is first argument
key = sys.argv[1]

mc = memcache.Client(memcached_address, debug=1)
print(mc.get(key))
