from pytest import mark

@mark.phase('dev')
def test_phase_is_dev(app_config):
    expect_url = "https://dev.com"
    expect_port = 8080

    base_url = app_config.base_url
    port = app_config.app_port

    assert base_url == expect_url
    assert port == expect_port

@mark.phase('sdb')
def test_phase_is_sandbox(app_config):
    expect_url = "https://sdb.com"
    expect_port = 8000

    base_url = app_config.base_url
    port = app_config.app_port

    assert base_url == expect_url
    assert port == expect_port

@mark.phase('beta')
def test_phase_is_beta(app_config):
    expect_url = "https://beta.com"
    expect_port = 80

    base_url = app_config.base_url
    port = app_config.app_port

    assert base_url == expect_url
    assert port == expect_port

@mark.phase('prod')
def test_phase_is_production(app_config):
    expect_url = "https://prod.com"
    expect_port = 80

    base_url = app_config.base_url
    port = app_config.app_port

    assert base_url == expect_url
    assert port == expect_port
