import sys


from src import Main


class Remove(Main):

    def remove(self, server_name_to_remove: str):
        actual_servers = []
        new_http_block = {}
        for server_block in self._servers:
            for server_tuple in server_block["value"]:
                if not isinstance(server_tuple, tuple):
                    continue
                if server_tuple[0] == "server_name":
                    if server_tuple[1] != server_name_to_remove:
                        actual_servers.append(server_block)
                    else:
                        print(f"Сервер {server_name_to_remove} удалён")
            new_http_block = self._http_block
            new_http_block["value"] = actual_servers
        self._update_http_block(new_block=new_http_block)



if __name__ == "__main__":
    nginx_conf_path = sys.argv[1]
    server_name = sys.argv[2]
    remove = Remove(nginx_conf_path=nginx_conf_path)
    remove.remove(server_name_to_remove=server_name)
