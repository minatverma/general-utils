#!/usr/bin/python

from __future__ import print_function
import subprocess


def run_os_command(cmd):
    """ takes unix/linux os command and returns output as text
    if cmd id successfully run then out contains output
    else error is captured in err"""
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out, err

#TODO
def get_database_name():
    """returns the database name running in the cluster/node"""

    return db_name


#TODO
def get_node_list():
    """returns a list of tuple with node_address and status as items"""
    node_list = list()
    cmd = "/opt/vertica/bin/admintools -t list_allnodes"
    out, err = run_os_command(cmd)
    if out:
        #node extraction logic goes here
    else:
        print("Error occured: {}".format(err))
    return node_list


#TODO
def restart_nodes(node_list):
    """Input : list of tuples with nodes name and status
    restarts all the nodes which is in `down` state
    returns exit code"""
    for nodes in node_list:
        if nodes[1] == 'Down':
        cmd = "/opt/vertica/bin/admintools -t start_db  -d " + db_name
