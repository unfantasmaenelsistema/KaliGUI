from tools.base import Tool, ToolField, FieldOption

_URL_PATTERN = r"https?://[\w.\-]+(:\d+)?(/[\w.\-/?=&%#]*)?"

class SqlmapTool(Tool):
    name = "sqlmap"
    description = "Detección y explotación automática de SQL injection"
    category = "vuln"
    icon = "💉"
    fields = [
        ToolField("url", "URL objetivo", "text", required=True,
                  placeholder="http://192.168.1.10/page.php?id=1",
                  pattern=_URL_PATTERN,
                  pattern_msg="Introduce una URL válida con parámetros. Ejemplo: http://host/page.php?id=1",
                  group="Target"),
        ToolField("data", "Datos POST", "text",
                  placeholder="user=test&pass=test",
                  help="Para peticiones POST, pegar aquí los parámetros", group="Target"),
        ToolField("cookie", "Cookie de sesión", "text",
                  placeholder="PHPSESSID=abc123; token=xyz",
                  help="Si la página requiere autenticación", group="Target"),
        ToolField("level", "Nivel (1-5)", "select", default="1",
                  options=[FieldOption(f"Nivel {i}", str(i)) for i in range(1, 6)],
                  help="Mayor nivel = más tests, más lento", group="Options"),
        ToolField("risk", "Riesgo (1-3)", "select", default="1",
                  options=[FieldOption(f"Riesgo {i}", str(i)) for i in range(1, 4)],
                  help="Mayor riesgo = payloads más agresivos", group="Options"),
        ToolField("dbs", "Enumerar bases de datos", "checkbox", default=False, group="Enumeration"),
        ToolField("dump", "Volcar tablas", "checkbox", default=False, group="Enumeration"),
        ToolField("batch", "Modo automático (--batch)", "checkbox", default=True,
                  help="No hace preguntas interactivas", group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--tables -D nombre_db", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["sqlmap", "-u", params["url"]]
        cmd += ["--level", str(params.get("level", 1))]
        cmd += ["--risk", str(params.get("risk", 1))]
        if params.get("data"):
            cmd += ["--data", params["data"]]
        if params.get("cookie"):
            cmd += ["--cookie", params["cookie"]]
        if params.get("dbs"):
            cmd.append("--dbs")
        if params.get("dump"):
            cmd.append("--dump")
        if params.get("batch"):
            cmd.append("--batch")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        return cmd
