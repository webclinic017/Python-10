from pytest import mark


@mark.body
class BodyTests:
    
    @mark.smoke
    def test_body(self):
        assert True

    def test_bumper(self):
        assert True

    def test_door(self):
        assert True        