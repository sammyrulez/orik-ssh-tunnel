import logging
import sys
import rumps
from orik.config_manager import ConfigReader, AppConfigManager
import paramiko
from sshtunnel import SSHTunnelForwarder


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class OrikBarApp(rumps.App):

    def _find_config(self, menu_title):
        for conf in self.configs:
            if menu_title.startswith(conf.host):
                logging.info(conf.forewards)
                for forward in conf.forewards:
                    if menu_title.endswith(forward.code()):
                        return (conf, forward)
        return (None, None)

    def _host_callback(self, menu_item):
        logging.info("click %s %s", menu_item.title, menu_item.state)

        if menu_item.state:
            if menu_item.title in self._running_tunnels.keys():
                self._running_tunnels[menu_item.title].stop()
                self._running_tunnels[menu_item.title] = None
            menu_item.state = 0
        else:
            logging.info("Init tunnel ")
            conf, forward = self._find_config(menu_item.title)

            if conf:
                logging.info("tunnel host: %s, user, forward host %s:%d",
                             conf.host_name, conf.user, forward.host, int(forward.remote_port))
                server = SSHTunnelForwarder(
                    conf.host_name,
                    ssh_username=conf.user,
                    remote_bind_address=(forward.host, forward.remote_port),
                    local_bind_address=("0.0.0.0", forward.local_port),
                    # ssh_password="xyz"
                )
                server.start()
                logging.info(server.local_bind_port)
                self._running_tunnels[menu_item.title] = server
                menu_item.state = 1
                # action_item = rumps.MenuItem(
                #    "Go -> ", callback=lambda x: print(str(x)))
                #self.menu.insert_after(menu_item.title, action_item)
                logging.info("DONE")

    def __init__(self):
        super(OrikBarApp, self).__init__(
            "Orik", icon='./dwarf-helmet.png', )
        self.menu = []
        self._running_tunnels = {}
        cr = ConfigReader()
        self.configs = cr.read_config()
        app_cfg = AppConfigManager()
        app_cfg.write_file_from_config(self.configs)  # TODO SYNC FUNCTION
        self.configs = app_cfg.read_file()
        for config in self.configs:
            for forward in config.forewards:
                self.menu.add(rumps.MenuItem(
                    title=config.host + " " + forward.display_label(), callback=self._host_callback))


if __name__ == "__main__":
    OrikBarApp().run()
