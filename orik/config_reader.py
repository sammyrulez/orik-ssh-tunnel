
from os.path import expanduser
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class HostConfig(object):
    def __init__(self):
        self.host = ""
        self.local_port = 0
        self.remote_port = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}:{} -> {}".format(self.host, self.remote_port, self.local_port)


class UserConfig(object):

    def __init__(self):
        self.host = ""
        self.host_name = ""
        self.user = ""
        self.forewards = list()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'host:{}, host name: {}, user: {}, forewards : \n {} '.format(self.host, self.host_name, self.user, self.forewards)


class ConfigReader(object):

    def read_config(self, config_file=expanduser("~")+"/.ssh/config"):
        logging.info("Reading from %s", config_file)
        configs = []
        with open(config_file, 'r') as config_data:
            lines = config_data.readlines()
            user_config = None
            i = 0
            for line in lines:
                if line.startswith('Host'):
                    configs.append(user_config)
                    user_config = UserConfig()
                    user_config.host = line[len('Host '):].strip()

                if line.find('HostName') > -1:
                    user_config.host_name = line[line.find(
                        'HostName') + len('HostName'):].strip()

                if line.find('User') > -1:
                    user_config.user = line[line.find(
                        'User') + len('User'):].strip()

                if line.find('Localforward') > -1:
                    host_data = str(line).strip().split(' ')[1:]
                    logging.info(host_data)
                    host_cfg = HostConfig()
                    host_cfg.host = host_data[1].split(':')[0]
                    host_cfg.remote_port = int(host_data[1].split(':')[1])
                    host_cfg.local_port = int(host_data[0])
                    user_config.forewards.append(host_cfg)
                    logging.info(user_config)

        configs.append(user_config)
        configs = list(filter(lambda x: x and len(x.forewards), configs))
        logging.info("configs %s", configs)
        return configs
