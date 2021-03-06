import logging
import sys
import subprocess
import rumps
from orik.config_manager import AppConfigManager, APP_HOME
from orik import ssh_manager
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

    def _write_to_clipboard(self, output):
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(output.encode('utf-8'))

    def _ask_window(self, menu_item, has_cancel_btn):
        msg_window = rumps.Window(
            message="Do you want to stop ssh tunneling with " + menu_item.title + " ?", title="Orik", cancel=has_cancel_btn, dimensions=[0, 0])
        msg_window.add_button("Copy url")
        response = msg_window.run()
        return response

    def _host_callback(self, menu_item):
        logging.info("click %s %s", menu_item.title, menu_item.state)
        conf, forward = self._find_config(menu_item.title)

        if menu_item.state:
            response = self._ask_window(menu_item, True)
            logging.info(response.clicked)
            if response.clicked == 1:
                if menu_item.title in self._running_tunnels.keys():
                    server = self._running_tunnels[menu_item.title]
                    ssh_manager.stop_tunnel(server)
                    self._running_tunnels[menu_item.title] = None
                menu_item.state = 0
            self._check_copy_btn(response, menu_item, forward)

        else:
            logging.info("Init tunnel ")
            if conf:
                logging.info("tunnel host: %s, user %s , forward host %s:%d",
                             conf.host_name, conf.user, forward.host, int(forward.remote_port))
                try:
                    server = ssh_manager.start_tunnel(conf, forward)
                    self._running_tunnels[menu_item.title] = server
                    response = self._ask_window(menu_item, False)
                    logging.info(response.clicked)
                    self._check_copy_btn(response, menu_item, forward)

                except Exception as e:
                    logging.error(str(e))
                    error_window = rumps.Window(
                        message=" Ssh tunnel  error : " + str(e), title="Orik", dimensions=[0, 0])
                    error_window.run()
                menu_item.state = 1
                logging.info("DONE")

    def _check_copy_btn(self, response, menu_item, forward):
        if response.clicked == 2:
            self._write_to_clipboard(self._format_url(menu_item, forward))

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
