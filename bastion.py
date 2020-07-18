#!/usr/bin/env python

import re
import time
import sys
import datetime
import paramiko
import traceback
import logging

DEBUG = 1

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def log(message):
    print("%s" % message)


def debug(message):
    if DEBUG > 0:
        log("debug: %s" % message)


class Bastion:
    def __init__(self, bastion_ip, bastion_pass):
        self.bastion_ip = bastion_ip
        self.bastion_pass = bastion_pass

    def run_scp_cmd(self, cloud_ip, passwd, file):

        scp_opt = ''
#        if DEBUG:
#            scp_opt="-v"

        debug("[%s] trying scp a file from bastion %s to cloud server %s" %
              (cloud_ip, self.bastion_ip, cloud_ip))

        cmd = 'scp -q ' + scp_opt + ' -o UserKnownHostsFile=/dev/null -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no %s root@%s:~/; echo scp status $? done.' % \
            (file, cloud_ip)

        debug("[%s] cmd=%s" % (cloud_ip, cmd))

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.bastion_ip, username='samuele.reghenzi')

        chan = ssh.invoke_shell()
        chan.settimeout(30)

        # wait for the prompt
        buff = ''
        while not buff.endswith(':~# '):
            resp = chan.recv(9999)
            buff += resp
            debug("[%s] %s" % (cloud_ip, resp))

        # Ssh and wait for the password prompt.
        chan.send(cmd + '\n')

        buff = ''
        still_waiting_for_data = True
        is_conn_lost = False
        is_timeout = False
        is_passwd = False
        is_route = False
        is_script_missing = False

        while still_waiting_for_data:
            resp = chan.recv(9999)
            buff += resp
            debug("[%s] %s" % (cloud_ip, resp))

            if buff.endswith('\'s password: '):
                is_passwd = True

            elif buff.find('Connection timed out') > -1:
                is_timeout = True

            elif buff.find('lost connection') > -1:
                is_conn_lost = True

            elif buff.find('No route to host') > -1:
                is_route = True

            elif buff.find('No such file or directory') > -1:
                is_script_missing = True

            still_waiting_for_data = not (
                is_timeout or is_conn_lost or is_passwd or is_route or is_script_missing)

        debug("[%s] is_timeout=%s, is_conn_lost=%s, is_passwd=%s is_route=%s is_script_missing=%s" %
              (cloud_ip, is_timeout, is_conn_lost, is_passwd, is_route, is_script_missing))

        if is_script_missing:
            log("ERROR, scp didn't succeed")
            sys.exit(-1)

        if is_passwd:
            # Send the password and wait for a prompt.
            time.sleep(3)
            debug("[%s] sending pass for scp: <%s> " % (cloud_ip, passwd))
            chan.send(passwd + '\n')

            buff = ''
            while buff.find(' done.') < 0:
                resp = chan.recv(9999)
                buff += resp
                debug("[%s] %s" % (cloud_ip, resp))

                if buff.find('Connection timed out') > -1 or buff.find('lost connection') > -1:
                    debug("[%s] scp aborted" % cloud_ip)
                    break

            ret = re.search('scp status (\d+) done.', buff).group(1)
            ssh.close()

            debug("[%s] did scp execution succeeded: %s (%s)" %
                  (cloud_ip, str(ret == '0'), ret))

            if 0 == int(ret):
                return True

        return False

    def run_ssh_cmd(self, cloud_ip, passwd, command):
        ssh_opt = ""
        cmd_opt = ""
#        if DEBUG:
#            ssh_opt="-v"
#            cmd_opt="debug"

        debug("[%s] trying to execute a command on bastion host %s for the cloud server %s" %
              (cloud_ip, self.bastion_ip, cloud_ip))

        cmd = 'ssh -t %s -o UserKnownHostsFile=/dev/null -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no root@%s "%s %s"; echo ssh status $? done.' % \
            (ssh_opt, cloud_ip, command, cmd_opt)

        debug("[%s] cmd=%s" % (cloud_ip, cmd))

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.bastion_ip, username='samuele.reghenzi')

        chan = ssh.invoke_shell()
        chan.settimeout(30)

        buff = ''
        while not buff.endswith(':~# '):
            resp = chan.recv(9999)
            buff += resp
            debug("[%s] %s" % (cloud_ip, resp))

        # Ssh and wait for the password prompt.
        chan.send(cmd + '\n')

        buff = ''
        still_waiting_for_data = True
        is_conn_lost = False
        is_timeout = False
        is_passwd = False
        is_route = False

        while still_waiting_for_data:
            resp = chan.recv(9999)
            buff += resp
            debug("[%s] %s" % (cloud_ip, resp))

            if buff.endswith('\'s password: '):
                is_passwd = True

            elif buff.find('Connection timed out') > -1:
                is_timeout = True

            elif buff.find('lost connection') > -1:
                is_conn_lost = True

            elif buff.find('No route to host') > -1:
                is_route = True

            still_waiting_for_data = not (
                is_timeout or is_conn_lost or is_passwd or is_route)

        debug("[%s] is_timeout=%s, is_conn_lost=%s, is_passwd=%s is_route=%s" %
              (cloud_ip, is_timeout, is_conn_lost, is_passwd, is_route))

        if is_passwd:
            # Send the password and wait for a prompt.
            time.sleep(3)
            debug("[%s] sending pass for ssh: <%s> " % (cloud_ip, passwd))
            chan.send(passwd + '\n')

            buff = ''
            while buff.find(' done.') < 0:
                resp = chan.recv(9999)
                buff += resp
                debug("[%s] %s" % (cloud_ip, resp))

                if buff.find('Connection timed out') > -1 or buff.find('lost connection') > -1 or \
                   buff.find('No route to host') > -1:

                    debug("[%s] ssh aborted" % cloud_ip)
                    break

            try:
                ret = re.search('ssh status (\d+) done\.', buff).group(1)

            except Exception:
                log("ERROR, exception when parsing ssh output")
                debug(traceback.format_exc())

            ssh.close()

            debug("[%s] ssh execution returned: %s " % (cloud_ip, ret))

            if int(ret) == 0:
                return True

            else:
                return False


if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('52.213.9.19', username='samuele.reghenzi')
    transport = paramiko.Transport(('', ssh_port))
    time.sleep(60)
