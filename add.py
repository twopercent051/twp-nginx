import sys


from src import Main


class Add(Main):

    @staticmethod
    def __backend_template(suffix: int) -> list[dict]:
        return [
            {
                "name": "location",
                "param": "/api/",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{8000 + suffix}"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                ],
            },
            {
                "name": "location",
                "param": "/docs/",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{8000 + suffix}/docs"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                    ("proxy_redirect", "/ /docs/"),
                ],
            },
            {
                "name": "location",
                "param": "/docs/authorization",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{8000 + suffix}/api/authorization"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                    ("proxy_redirect", "/ /docs/"),
                ],
            },
            {
                "name": "location",
                "param": "/openapi.json",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{8000 + suffix}/openapi.json"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                ],
            },
        ]

    @staticmethod
    def __frontend_template(suffix: int) -> list[dict]:
        return [
            {
                "name": "location",
                "param": "/",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{3000 + suffix}"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                ],
            },
            {
                "name": "location",
                "param": "/api/_content/",
                "value": [
                    ("proxy_pass", f"http://127.0.0.1:{3000 + suffix}"),
                    ("proxy_set_header", "Host $host"),
                    ("proxy_set_header", "X-Real-IP $remote_addr"),
                    (
                        "proxy_set_header",
                        "X-Forwarded-For $proxy_add_x_forwarded_for",
                    ),
                    ("proxy_set_header", "X-Forwarded-Proto $scheme"),
                ],
            },
        ]

    @staticmethod
    def __server_template(server_name_to_add: str, backend: list[dict], frontend: list[dict]) -> dict:
        return {
            "name": "server",
            "param": "",
            "value": [
                ("server_name", server_name_to_add),
            ]
            + backend
            + frontend,
        }

    def add(self, server_name_to_add: str, locations: str):

        if locations not in ["bf", "f", "b", "fb"]:
            print("Неправильный аргумент")
            return
        try:
            servers_info = self._get_servers_ports()
            servers = self._servers
        except AttributeError:
            servers_info = []
            servers = []
        suffix = 0
        if len(servers_info) > 0:
            suffix = servers_info[-1]["suffix"] + 1
        backend = self.__backend_template(suffix=suffix) if "b" in locations else []
        frontend = self.__frontend_template(suffix=suffix) if "f" in locations else []
        server = self.__server_template(server_name_to_add=server_name_to_add, backend=backend, frontend=frontend)
        servers.append(server)
        http_block = self._http_block
        http_block["value"] = servers
        self._update_http_block(new_block=http_block)
        print(f"Добавили {server_name_to_add}")


if __name__ == "__main__":
    nginx_conf_path = sys.argv[1]
    server_name = sys.argv[2]
    locs = sys.argv[3]
    add = Add(nginx_conf_path=nginx_conf_path)
    add.add(server_name_to_add=server_name, locations=locs)
