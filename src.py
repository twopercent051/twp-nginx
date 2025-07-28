import re
from pathlib import Path


class Main:
    def __init__(self, url: str):
        self._url = url
        # Пути по умолчанию можно заменить на свои, если надо
        self.__nginx_conf_path = Path("./.nginx_conf_backups/nginx.conf")
        self._sites_available_path = Path(f"./.nginx_conf_backups/sites-available/{url}")

    @staticmethod
    def _http_block_str() -> str:
        # Твой эталонный http-блок, можно кастомизировать если нужно
        return """
http {
    include       mime.types;
    default_type  application/octet-stream;
    access_log    /var/log/nginx/access.log  combined;
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
""".strip()

    def _reset_http_block(self):
        """
        Заменяет http-блок в nginx.conf на шаблонный. Оставляет все остальные секции как есть.
        """
        conf_path = self.__nginx_conf_path
        http_block = self._http_block_str()

        content = conf_path.read_text(encoding="utf-8")

        # Заменяем первый попавшийся http {...}
        new_content, n = re.subn(r"http\s*\{.*?\}", http_block, content, flags=re.DOTALL)

        if n == 0:
            # Если нет http блока - добавим в конец файла
            if not new_content.endswith("\n"):
                new_content += "\n"
            new_content += http_block + "\n"

        conf_path.write_text(new_content, encoding="utf-8")

    def _update_available_site(self, template_text: str):
        """
        Перезаписывает sites-available файл содержимым из строки (обычно server { ... })
        """
        path = self._sites_available_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template_text.strip() + "\n", encoding="utf-8")
