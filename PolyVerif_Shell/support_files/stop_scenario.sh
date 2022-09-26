#!/bin/bash

pid=3353

value=`cat pidfile`
per_node_pid=`cat Poly_Suite/per_node_pid`
 
echo "PID about to stop : $pid"
kill -9 $per_node_pid
kill -9 $pid
echo $value
kill -KILL -$value


exit


