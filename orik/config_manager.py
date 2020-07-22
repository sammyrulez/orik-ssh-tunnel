
from os.path import expanduser
from os import path
import os
import logging
import sys
import csv
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
home = expanduser("~")


class HostConfig(object):
    def __init__(self):
        self.host = ""
        self.local_port = 0
        self.remote_port = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}:{} -> {}".format(self.host, self.remote_port, self.local_port)

    def code(self):
        return self.host + ":" + str(self.remote_port) + " -> " + str(self.local_port)


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


class AppConfig(HostConfig):

    def __init__(self):
        self.custom_cert = ""
        self.ask_for_password = False
        self.label = None
        self.protocol = None
        super().__init__()

    def display_label(self):
        if self.label:
            return self.label
        else:
            return self.code()


CSV_HEADERS = ["Bastion", "Host Name", "User", "Remote Host", "Remote Port",
               "Local Port", "Alias", "Protocol", "Ask for password", "Custom cert"]
SETTINGS_PATH = home+'/.orik_ssh/config.csv'


class AppConfigManager(object):

    def sync_file_from_config(self,  settings_file_path=SETTINGS_PATH):

        cr = ConfigReader()
        ssh_configs = cr.read_config()

        setting_dir = path.dirname(settings_file_path)
        logging.info(setting_dir)
        if not path.exists(setting_dir):
            os.makedirs(setting_dir)
            with open(settings_file_path, 'w') as cfg_file:
                writer = csv.writer(cfg_file)
                writer.writerow(CSV_HEADERS)
                for cfg in ssh_configs:
                    for fwd in cfg.forewards:
                        writer.writerow(
                            (cfg.host, cfg.host_name, cfg.user, fwd.host, fwd.local_port, fwd.remote_port))
        else:
            with open(settings_file_path, 'ra') as cfg_file:
                cfg_file_reader = list(csv.reader(cfg_file.readlines()[1:]))
                writer = csv.writer(cfg_file)
                for cfg in ssh_configs:
                    for app_cfg in cfg_file_reader:
                        if cfg.host != app_cfg[0]:
                            writer.writerow(
                                (cfg.host, cfg.host_name, cfg.user, fwd.host, fwd.local_port, fwd.remote_port))
        return self.read_file(settings_file_path)

    def read_file(self, settings_file_path=SETTINGS_PATH):
        configs = []
        with open(settings_file_path, 'r') as cfg_file:
            cfg_file_reader = csv.reader(cfg_file.readlines()[1:])
            uc = UserConfig()
            for row in cfg_file_reader:
                logging.info(" row: |%s| %s %s", uc.host, row[0], row[3])
                if uc.host and row[0] != uc.host:
                    configs.append(uc)
                    uc = UserConfig()
                uc.host = row[0]
                uc.host_name = row[1]

                uc.user = row[2]
                ac = AppConfig()
                ac.host = row[3]
                ac.remote_port = row[4]
                ac.local_port = row[5]
                ac.label = row[6]
                ac.protocol = row[7]
                ac.ask_for_password = row[8]
                ac.custom_cert = row[9]
                uc.forewards.append(ac)
            configs.append(uc)
        return configs
