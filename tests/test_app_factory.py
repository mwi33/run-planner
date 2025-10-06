def test_app_factory(app_instance):
    assert app_instance is not None
    assert app_instance.testing is False
