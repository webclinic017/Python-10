from pytest import mark

@mark.ui
class UiTests:
    def test_naver(self, chrome_browser):
        chrome_browser.get("https://www.naver.com")
        assert True

    def test_kakao(self, chrome_browser):
        chrome_browser.get("https://www.kakao.com")
        assert True
        
    def test_google(self, chrome_browser):
        chrome_browser.get("https://www.google.com")
        assert True