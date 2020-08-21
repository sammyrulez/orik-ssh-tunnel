import logging
import sys
import rumps
from orik.config_manager import AppConfigManager, APP_HOME
import paramiko
from sshtunnel import SSHTunnelForwarder


def _init_logging_():
    logger = logging.getLogger('spam_application')
    fh = logging.FileHandler(APP_HOME+'orik.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)


format_fns = {
    'http': lambda x: "http://localhost:" + x.remote_port,
    'https': lambda x: "https://localhost:" + x.remote_port,
    'ssh': lambda x: "ssh -p" + x.remote_port + " " + x.user + "@localhost",
    'default': lambda x: "localhost:" + x.remote_port
}


class OrikBarApp(rumps.App):

    def _find_config(self, menu_title):
        for conf in self.configs:
            if menu_title.startswith(conf.host):
                logging.info(conf.forewards)
                for forward in conf.forewards:
                    logging.info("item x = %s %s %s", menu_title,
                                 forward.display_label(), str(menu_title.endswith(forward.display_label())))
                    if forward.display_label() in menu_title:
                        return (conf, forward)
        return (None, None)

    def _host_callback(self, menu_item):
        logging.info("click %s %s", menu_item.title, menu_item.state)
        conf, forward = self._find_config(menu_item.title)

        if menu_item.state:
            msg_window = rumps.Window(
                message="Do you want to stop ssh tunneling with " + menu_item.title + " ?", title="Orik", cancel=True, dimensions=[320, 32], default_text=self._format_url(menu_item, forward))
            response = msg_window.run()
            if response.clicked:
                if menu_item.title in self._running_tunnels.keys():
                    server = self._running_tunnels[menu_item.title]
                    self.stop_tunnel(server)
                    self._running_tunnels[menu_item.title] = None
                menu_item.state = 0
        else:
            logging.info("Init tunnel ")
            if conf:
                logging.info("tunnel host: %s, user %s , forward host %s:%d",
                             conf.host_name, conf.user, forward.host, int(forward.remote_port))
                try:
                    server = self.start_tunnel(conf, forward)
                    newvariable284 = server
                    menu_item.state = 1
                    msg_window = rumps.Window(
                        message=menu_item.title + " ssh tunnel activated", title="Orik", dimensions=[320, 32], default_text=self._format_url(menu_item, forward))
                    msg_window.run()
                    logging.info("DONE")
                except Exception as e:
                    logging.error(str(e))
                    error_window = rumps.Window(
                        message=" Ssh tunnel  error : " + str(e), title="Orik", dimensions=[0, 0])
                    error_window.run()

    def _format_url(self, menu_item, forward):

        if forward.protocol:
            return format_fns[forward.protocol](forward)
        else:
            return format_fns['default'](forward)

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
    _init_logging_()
    OrikBarApp().run()
