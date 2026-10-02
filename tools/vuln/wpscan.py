from tools.base import Tool, ToolField, FieldOption

_URL_PATTERN = r"https?://[\w.\-]+(:\d+)?(/[\w.\-/?=&%#]*)?"


class WPScanTool(Tool):
    name = "wpscan"
    description = "Escáner de vulnerabilidades para WordPress"
    category = "vuln"
    icon = "🔑"
    fields = [
        ToolField("url", "URL del WordPress", "text", required=True,
                  placeholder="http://192.168.1.10/wordpress",
                  pattern=_URL_PATTERN,
                  pattern_msg="Introduce la URL completa del WordPress.",
                  group="Target"),
        ToolField("enumerate", "Enumerar", "multiselect",
                  options=[
                      FieldOption("u  — usuarios", "u"),
                      FieldOption("p  — plugins vulnerables", "p"),
                      FieldOption("ap — todos los plugins", "ap"),
                      FieldOption("t  — themes vulnerables", "t"),
                      FieldOption("at — todos los themes", "at"),
                      FieldOption("tt — timthumbs", "tt"),
                      FieldOption("cb — config backups", "cb"),
                      FieldOption("dbe — DB exports", "dbe"),
                  ],
                  help="Dejar vacío para enumeración por defecto",
                  group="Enumeration"),
        ToolField("brute_users", "Fuerza bruta de usuarios", "checkbox",
                  default=False, group="BruteForce"),
        ToolField("passwords", "Wordlist de contraseñas", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Solo si activas fuerza bruta",
                  group="BruteForce"),
        ToolField("api_token", "WPScan API Token", "text",
                  placeholder="tu_token_aqui",
                  help="Opcional. Necesario para ver CVEs. Registro gratuito en wpscan.com",
                  group="Auth"),
        ToolField("no_tls_verify", "No verificar TLS", "checkbox",
                  default=False, group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--request-timeout 60 --throttle 200",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["wpscan", "--url", params["url"]]

        if params.get("enumerate"):
            vals = params["enumerate"] if isinstance(params["enumerate"], list) else [params["enumerate"]]
            if vals:
                cmd += ["--enumerate", ",".join(vals)]

        if params.get("brute_users") and params.get("passwords"):
            cmd += ["--passwords", params["passwords"]]

        if params.get("api_token"):
            cmd += ["--api-token", params["api_token"]]
        if params.get("no_tls_verify"):
            cmd.append("--disable-tls-checks")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        return cmd
