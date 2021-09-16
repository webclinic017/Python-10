class Config:
    def __init__(self, phase):
        self.base_url = {'dev': 'http://dev.com','qa': 'http://qa.com'}[phase]
        self.app_port = {
            'dev': 8080,
            'qa': 80
        }[phase]
        