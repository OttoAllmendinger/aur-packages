#!/bin/bash
#
# Author: Otto Allmendinger <otto.allmendinger at googlemail dot com>
# Date: 2009-12-14
# Description: Murmur wrapper script for pivilige separation
#

ARGS="-ini /etc/murmur.ini $@"
su -c "/usr/lib/murmur/murmur ${ARGS}" - murmur
