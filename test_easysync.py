from easysync import AppConfig
import os


def test_create_config():
    a = AppConfig()
    a.config_setup('Testapp')
    assert a.config is not None
    tc = {'section': {'key': 'value'}}
    assert a.get_default_config() == tc
    assert os.path.isfile(
        a.get_config_path()
    ) == True, 'Test config should be created by config_setup()'

def test_delete_config():
    a = AppConfig()
    a.config_setup('Testapp')
    assert os.path.isfile(
        a.get_config_path()
    ) == True, 'Test config does not exist, cannot delete'
    a.purge_config()
    assert os.path.isfile(
        a.get_config_path()
    ) == False
