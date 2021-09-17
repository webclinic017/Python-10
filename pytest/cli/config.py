from typing import Tuple


class Config:
    phases = tuple(['dev', 'sdb', 'beta','prod']) # sdb:sandbox, prod:production
    url_mapper = {phase: f"https://{phase}.com" for phase in phases}
    port_mapper = {phase: port for phase, port in zip(phases, [8080, 8000,80,80])}

    def __init__(self, phase): 
        self.base_url = Config.url_mapper[phase]
        self.app_port = Config.port_mapper[phase]
