Nagios SNMP Location
====================

Nagios collects SNMP location of devices, saves it using memcached and displays it in notifications.

Requirements
------------

* Nagios
* Net-SNMP with python bindings
* Memcached
* py-memcached

Installation
------------
Put the Nagios plugin in the directory configured in resource.cfg, for example:
<pre>
# Sets $USER1$ to be the path to the plugins
$USER1$=/usr/local/libexec/nagios
</pre>

Define a check command in commands.cfg (SNMP community 'public' used below):
<pre>
# 'check_snmp_location' command definition
define command{
    command_name    check_snmp_location
    command_line    $USER1$/check_snmp_location.py -H $HOSTADDRESS$ -C public
}
</pre>

Create service checks for location, such as following:
<pre>
define service{
    use                     trivial-service   # Notifications disabled
    host_name               switch
    service_description     SNMP Location
    check_command           check_snmp_location
}
</pre>

__Make sure the user Nagios runs as can execute the script properly__
<pre>
nagios# su -m nagios -c '/usr/local/libexec/nagios/check_snmp_location.py -H switch -C public'
</pre>

If it looks like a permission problem, chmod/chown the file so Nagios can run it. If it complains about not being able to extract python eggs, it might be because the user cannot create a '.python-eggs' directory in its home folder. You can either fix home folder permissions or extract the relevant eggs manually. Note: directory below is where python lays its eggs in FreeBSD:
<pre>
cd /usr/local/lib/python2.7/site-packages
mkdir egg-archive
unzip netsnmp_python-*.egg
mv netsnmp_python-*.egg ./egg-archive/
unzip python_memcached-*.egg
mv python_memcached-*.egg ./egg-archive/
</pre>
