#!/bin/bash

# Find how many VMs are available for execution
# Also notify which VMs are down
# Author: Giacomo Mc Evoy - giacomo@lncc.br
# LNCC Brazil 2013

# Count free VMs
FREE=$(qnodes | grep 'state = free' | wc -l)
echo "$FREE VMs are free"

# Count down VMs and show their names if needed
DOWN=$(qnodes | grep 'state = down' | wc -l)
if [[ $DOWN -ne '0' && $FREE -ne '0' ]]; then  
  echo 
  echo "The following VMs are down:"
  qnodes | grep -B 1 'state = down' | grep -v 'state = down' | grep -v '\-\-'
fi
