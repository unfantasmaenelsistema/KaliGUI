from tools.base import Tool, ToolField, FieldOption

_URL_PATTERN = r"https?://[\w.\-]+(:\d+)?(/[\w.\-/?=&%#]*)?"


class GobusterTool(Tool):
    name = "gobuster"
    description = "Fuzzing de directorios, ficheros y virtual hosts"
    category = "recon"
    icon = "💥"
    fields = [
        ToolField("mode", "Modo", "select", required=True, default="dir",
                  options=[
                      FieldOption("dir  — directorios y ficheros", "dir"),
                      FieldOption("dns  — subdominios DNS", "dns"),
                      FieldOption("vhost — virtual hosts", "vhost"),
                      FieldOption("fuzz — fuzzing genérico", "fuzz"),
                  ], group="Target"),
        ToolField("url", "URL objetivo", "text", required=True,
                  placeholder="http://192.168.1.10",
                  pattern=_URL_PATTERN,
                  pattern_msg="Introduce una URL válida. Ejemplo: http://192.168.1.10",
                  group="Target"),
        ToolField("wordlist", "Wordlist", "text", required=True,
                  placeholder="/usr/share/wordlists/dirb/common.txt",
                  help="Ruta a la wordlist de directorios/rutas",
                  group="Target"),
        ToolField("extensions", "Extensiones (solo modo dir)", "text",
                  placeholder="php,html,txt,bak",
                  help="Extensiones a probar separadas por coma",
                  group="Options"),
        ToolField("status_codes", "Códigos HTTP a mostrar", "text",
                  default="200,204,301,302,307,401,403",
                  placeholder="200,301,302,403",
                  help="Códigos de respuesta que se consideran válidos",
                  group="Options"),
        ToolField("threads", "Threads", "number", default=10,
                  min_val=1, max_val=100,
                  help="Peticiones paralelas (10-30 recomendado)",
                  group="Options"),
        ToolField("follow_redirect", "Seguir redirecciones (-r)", "checkbox",
                  default=False, group="Options"),
        ToolField("no_tls_verify", "No verificar TLS (-k)", "checkbox",
                  default=False, group="Options"),
        ToolField("cookie", "Cookie de sesión", "text",
                  placeholder="PHPSESSID=abc123",
                  help="Si el objetivo requiere autenticación",
                  group="Auth"),
        ToolField("user_agent", "User-Agent", "text",
                  placeholder="Mozilla/5.0 ...",
                  help="Dejar vacío para usar el default de gobuster",
                  group="Auth"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--timeout 10s --delay 100ms",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        mode = params.get("mode", "dir")
        cmd = ["gobuster", mode]
        cmd += ["-u", params["url"]]
        cmd += ["-w", params["wordlist"]]

        if params.get("extensions") and mode == "dir":
            cmd += ["-x", params["extensions"]]
        if params.get("status_codes"):
            cmd += ["-s", params["status_codes"]]
        if params.get("threads"):
            cmd += ["-t", str(params["threads"])]
        if params.get("follow_redirect"):
            cmd.append("-r")
        if params.get("no_tls_verify"):
            cmd.append("-k")
        if params.get("cookie"):
            cmd += ["-c", params["cookie"]]
        if params.get("user_agent"):
            cmd += ["-a", params["user_agent"]]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        return cmd
