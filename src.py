from pynginxconfig import NginxConfig
from urllib.parse import urlparse


class Main:
    def __init__(self, nginx_conf_path: str):
        cfg = NginxConfig()
        self.__cfg = cfg
        self.__nginx_conf_path = nginx_conf_path
        cfg.loadf(filename=nginx_conf_path)
        for entry in cfg.data:
            if isinstance(entry, dict) and entry.get("name") == "http":
                self._http_block = entry
                self._servers = entry["value"]


    def _update_http_block(self, new_block: dict):
        self.__cfg.remove([("http", "")])
        self.__cfg.append(new_block)
        self.__cfg.savef(self.__nginx_conf_path)


    def _get_servers_ports(self) -> list[dict]:
        result = []
        for server in self._servers:
            server_value = server.get("value")
            if not server_value:
                return result
            server_name = ""
            ports = []
            for location in server_value:
                if isinstance(location, tuple) and location[0] == "server_name":
                    server_name = location[1]
                if isinstance(location, dict) and location.get("name") == "location":
                    proxy_data = location.get("value")
                    if not proxy_data:
                        continue
                    for item in proxy_data:
                        if isinstance(item, tuple) and item[0] == "proxy_pass":
                            url = item[1]
                            port = urlparse(url=url).port
                            ports.append(port)
            ports = list(set(ports))
            backend = False
            frontend = False
            suffix = 0
            for port in ports:
                suffix = port % 100
                prefix = port // 1000
                if prefix == 3:
                    frontend = True
                if prefix == 8:
                    backend = True
            server_data = {"server_name": server_name, "ports": ports, "suffix": suffix, "backend": backend, "frontend": frontend}
            result.append(server_data)
        result = sorted(result, key=lambda x: x["suffix"])
        return result




