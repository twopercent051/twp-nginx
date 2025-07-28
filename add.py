import click

from pathlib import Path
from typing import Optional


class Add:
    def __init__(self, url: str):
        self._url = url
        self._sites_available_path = Path(f"./.nginx_conf_backups/sites-available/{url}")

    @staticmethod
    def __backend_template(port: Optional[int]) -> str:
        if not port:
            return ""
        return f"""
    location /api/ {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    location /docs/ {{
        proxy_pass http://127.0.0.1:{port}/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect / /docs/;
    }}
    location /docs/authorization {{
        proxy_pass http://127.0.0.1:{port}/api/authorization;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect / /docs/;
    }}
    location /openapi.json {{
        proxy_pass http://127.0.0.1:{port}/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}"""

    @staticmethod
    def __frontend_template(port: Optional[int]) -> str:
        if not port:
            return ""
        return f"""
    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    location /api/_content/ {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}"""

    def __server_template(self, backend: str, frontend: str) -> str:
        return f"""
server {{
    server_name {self._url};
{backend}{frontend}
    error_page 502 503 504 /50x.html;
    location = /50x.html {{
        root /usr/share/nginx/html;
    }}
    listen 80;
}}
""".strip()

    def add(self, backend_port: Optional[int] = None, frontend_port: Optional[int] = None):
        backend = self.__backend_template(port=backend_port)
        frontend = self.__frontend_template(port=frontend_port)
        server = self.__server_template(backend=backend, frontend=frontend)
        self._sites_available_path.parent.mkdir(parents=True, exist_ok=True)
        self._sites_available_path.write_text(server + "\n", encoding="utf-8")
        print(f"Добавили {self._url} в конфиг. Порты: {backend_port} {frontend_port}")


@click.command()
@click.option("--url", required=True, help="Домен/поддомен (обязательно)")
@click.option("-b", "--backend-port", type=int, help="Порт для backend (опционально)")
@click.option("-f", "--frontend-port", type=int, help="Порт для frontend (опционально)")
def main(url: str, backend_port: int | None, frontend_port: int | None):
    add = Add(url=url)
    add.add(backend_port=backend_port, frontend_port=frontend_port)


if __name__ == "__main__":
    main()
