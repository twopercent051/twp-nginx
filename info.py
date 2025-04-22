import sys


from src import Main


class Info(Main):

    def info(self):
        server_data = self._get_servers_ports()
        for server in server_data:
            backend = " BACKEND" if server["backend"] else ""
            frontend = " FRONTEND" if server["frontend"] else ""
            print(f"{server['server_name']}:{backend}{frontend} || {server['ports']}")


if __name__ == "__main__":
    nginx_conf_path = sys.argv[1]
    info = Info(nginx_conf_path=nginx_conf_path)
    info.info()
