from pytest import mark


@mark.parametrize('company', [
        ("naver"),
        ("kakao"),
        ("microsoft"),
        ("github")
    ]
)
def test_company_with_decorator_param(company):
    print(f"{company} is visited as expected")

def test_company_with_fixture_param(company):
    print(f"{company} is visited as expected")

def test_browser_can_navigate_to_company_homepage(browser, company):
    print("HI")
    browser.get(f'https://{company}.com')