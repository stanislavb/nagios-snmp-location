#!/usr/local/bin/python
# Authors: Stanislav Blokhin

# This script checks the standard SNMP location oid
# and saves it in a memcached database with hostname as key.
#
# FreeBSD requirements:
# Compile net-snmp with python bindings
# Install py-memcached

# Nagios exit codes:
# 0 OK
# 1 WARNING
# 2 CRITICAL
# 3 UNKNOWN

import netsnmp
import memcache
from optparse import OptionParser
from sys import exit

# Config
# Either hostname/IP or UNIX socket
memcached_address=['unix:/var/run/memcached/memcached.sock']
default_community="public"
location_oid='1.3.6.1.2.1.1.6'
snmp_version=2

# Command line option parsing and help text (-h)
usage="usage: %prog -H host_or_IP -C snmp_community"
parser = OptionParser(usage=usage)
parser.add_option("-H", "--host", dest="host", help="hostname or IP address")
parser.add_option("-C", "--community", dest="community", default=default_community, help="SNMP community")
(options, args) = parser.parse_args()

# We must have a host
if not options.host:
	print("UNKNOWN: No hostname or IP to check")
	exit(3) # UNKNOWN

# Let's get SNMP location
var = netsnmp.Varbind(location_oid,'0')
res = netsnmp.snmpget(var, Version=snmp_version, DestHost=options.host, Community=options.community, Retries=1)
location = res[0]

if location is not None:
	print("OK: " + location)

	# Memcached
	try:
		mc = memcache.Client(memcached_address, debug=0)
		mc.set(options.host, location)
	except Exception:
		# We don't care if memcached doesn't work
		pass
	exit(0) # OK

print("UNKNOWN: error for host " + options.host + " and SNMP community " + options.community)
exit(3) # UNKNOWN
