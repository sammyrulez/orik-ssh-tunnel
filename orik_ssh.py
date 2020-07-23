import logging
import sys
import rumps
from orik.config_manager import AppConfigManager
import paramiko
from sshtunnel import SSHTunnelForwarder


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class OrikBarApp(rumps.App):

    def _find_config(self, menu_title):
        for conf in self.configs:
            if menu_title.startswith(conf.host):
                logging.info(conf.forewards)
                for forward in conf.forewards:
                    logging.info("item x = %s %s %s", menu_title,
                                 forward.display_label(), str(menu_title.endswith(forward.display_label())))
                    if menu_title.endswith(forward.display_label()):
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
                logging.info("tunnel host: %s, user %s , forward host %s:%d",
                             conf.host_name, conf.user, forward.host, int(forward.remote_port))
                try:
                    server = SSHTunnelForwarder(
                        conf.host_name,
                        ssh_username=conf.user,
                        remote_bind_address=(
                            forward.host, int(forward.remote_port)),
                        local_bind_address=(
                            "0.0.0.0", int(forward.local_port)),
                        # ssh_password="xyz"
                    )
                    server.start()
                except Exception as e:
                    logging.error(str(e))
                logging.info(" SErver started %s", conf.host_name)
                self._running_tunnels[menu_item.title] = server
                menu_item.state = 1
                action_item = rumps.MenuItem(
                    self._clipboard_item(forward), callback=lambda x: print(str(x)))
                self.menu.insert_after(menu_item.title, action_item)
                logging.info("DONE")

    def _clipboard_item(self, forward):
        label = "\t"
        if forward.protocol:
            label = label + " copy url"
        else:
            label = label + " copy address and port"
        return label

    def __init__(self):
        super(OrikBarApp, self).__init__(
            "Orik", icon='./dwarf-helmet.png', )
        self.menu = []
        self._running_tunnels = {}

        app_cfg = AppConfigManager()
        self.configs = app_cfg.sync_file_from_config()

        for config in self.configs:
            for forward in config.forewards:
                self.menu.add(rumps.MenuItem(
                    title=config.host + " " + forward.display_label(), callback=self._host_callback))


if __name__ == "__main__":
    OrikBarApp().run()
