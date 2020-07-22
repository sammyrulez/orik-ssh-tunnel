from orik.config_manager import ConfigReader, AppConfigManager


class TestConfigReader:

    def test_reading_ssh_config(self):
        cr = ConfigReader()
        configs = cr.read_config(
            config_file='./config_fixture')
        assert len(configs) == 1
        assert configs[0].host == 'test-bastion'
        assert configs[0].user == 'jon.doe'

    def test_reading_app_config(self):
        app_cfg = AppConfigManager()
        app_cfg.read_file()

    def test_wrtie_from_config(self):
        cr = ConfigReader()
        configs = cr.read_config(
            config_file='./config_fixture')
        app_cfg = AppConfigManager()
        app_cfg.write_file_from_config(configs, "/tmp/vikingen/out.csv")
