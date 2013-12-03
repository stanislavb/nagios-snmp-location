Nagios SNMP Location
====================

Nagios collects SNMP location of devices, saves it using memcached and displays it in notifications.

Requirements
------------

* Nagios
* Net-SNMP with python bindings
* Memcached
* py-memcached

Installation of Nagios plugin
-----------------------------

**Installation and general configuration of Nagios and Memcached is out of scope of this document. This only covers necessary configuration to introduce SNMP location.**

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

__Make sure the user Nagios runs as can execute the script properly.__ If you access memcached through a UNIX socket, you might have to make memcached run as the nagios user so the socket file is accessible by Nagios.
<pre>
nagios# su -m nagios -c '/usr/local/libexec/nagios/check_snmp_location.py -H switch -C public'
</pre>

If it looks like a permission problem, chmod/chown the file so Nagios can run it. If it complains about not being able to extract python eggs, it might be because the user cannot create a '.python-eggs' directory in its home folder. You can either fix home folder permissions or extract the relevant eggs manually. I recommend moving the extracted contents to the location of the script, so subsequent compiles/installs don't generate a new .egg file and break functionality. Note: directory below is where python lays its eggs in FreeBSD:
<pre>
cd /usr/local/lib/python2.7/site-packages
unzip netsnmp_python-*.egg
unzip python_memcached-*.egg
cp -r /usr/local/lib/python2.7/site-packages/netsnmp /usr/local/libexec/nagios/
cp /usr/local/lib/python2.7/site-packages/memcache.py /usr/local/libexec/nagios/
</pre>

Notification integration
------------------------

We'd like to do something with the gathered information which is stored in memcached as a key:value pair with Nagios-defined host address as key and SNMP location as value.

Put the memcached_get.py script somewhere good, and modify Nagios notify command definitions in commands.cfg (change to fit your environment):
<pre>
# 'notify-host-by-email' command definition
define command{
        command_name    notify-host-by-email
        command_line    /usr/bin/printf "** Nagios System Surveillence **\n\nNotification Type: %b\nHost: %b\nState: %b\nAddress: %b\nInfo: %b\n\nDate/Time: %b\nLocation: %b" "$NOTIFICATIONTYPE$" "$HOSTNAME$" "$HOSTSTATE$" "$HOSTADDRESS$" "$HOSTOUTPUT$" "$LONGDATETIME$" "`/usr/local/bin/memcached_get.py $HOSTADDRESS$`" | /usr/bin/mail -s "Host $HOSTSTATE$ alert for $HOSTNAME$!" $CONTACTEMAIL$
}

# 'notify-by-email' command definition
define command{
        command_name    notify-by-email
        command_line    /usr/bin/printf "** Nagios System Surveillence **\n\nNotification Type: %b\n\nService: %b\nHost: %b\nAddress: %b\nState: %b\n\nDate/Time: %b\n\nAdditional Info:\n\n%b\nLocation: %b" "$NOTIFICATIONTYPE$" "$SERVICEDESC$" "$HOSTALIAS$" "$HOSTADDRESS$" "$SERVICESTATE$" "$LONGDATETIME$" "$SERVICEOUTPUT$" "`/usr/local/bin/memcached_get.py $HOSTADDRESS$`" | /usr/bin/mail -s "$NOTIFICATIONTYPE$ alert - $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$" $CONTACTEMAIL$
}
</pre>

FreeBSD license
---------------
Copyright (c) 2013, Stanislav Blokhin (github.com/stanislavb)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
