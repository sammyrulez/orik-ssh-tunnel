from orik.config_reader import ConfigReader


class TestConfigReader:

    def test_reading_sssh_config(self):
        cr = ConfigReader()
        configs = cr.read_config(
            config_file='/Users/sam/Projects/open/orik/config_fixture')
        assert len(configs) == 1
        assert configs[0].host == 'test-bastion'
        assert configs[0].user == 'jon.doe'
