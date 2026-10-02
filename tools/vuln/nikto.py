from tools.base import Tool, ToolField, FieldOption

_HOST_PATTERN = r"(https?://)?[\w.\-]+(:\d+)?(/[\w.\-/?=&%#]*)?"

class NiktoTool(Tool):
    name = "nikto"
    description = "Escáner de vulnerabilidades web (headers, configuraciones, CVEs)"
    category = "vuln"
    icon = "🕷️"
    fields = [
        ToolField("target", "Host/URL objetivo", "text", required=True,
                  placeholder="192.168.1.10 o http://192.168.1.10",
                  pattern=_HOST_PATTERN,
                  pattern_msg="Introduce una IP, hostname o URL válida.",
                  group="Target"),
        ToolField("port", "Puerto", "number",
                  placeholder="80",
                  min_val=1, max_val=65535,
                  help="Dejar vacío para usar el default (80/443)", group="Target"),
        ToolField("ssl", "Forzar SSL/HTTPS", "checkbox", default=False, group="Target"),
        ToolField("tuning", "Tuning (tipos de tests)", "multiselect",
                  options=[
                      FieldOption("1 - Interesting File / Seen in logs", "1"),
                      FieldOption("2 - Misconfiguration / Default File", "2"),
                      FieldOption("3 - Information Disclosure", "3"),
                      FieldOption("4 - Injection (XSS/Script/HTML)", "4"),
                      FieldOption("5 - Remote File Retrieval (inside webroot)", "5"),
                      FieldOption("6 - Denial of Service", "6"),
                      FieldOption("7 - Remote File Retrieval (server wide)", "7"),
                      FieldOption("8 - Command Execution / Remote Shell", "8"),
                      FieldOption("9 - SQL Injection", "9"),
                  ], help="Dejar vacío para todos los tests", group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-evasion 1", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["nikto", "-h", params["target"]]
        if params.get("port"):
            cmd += ["-p", str(params["port"])]
        if params.get("ssl"):
            cmd.append("-ssl")
        if params.get("tuning"):
            tuning = "".join(params["tuning"]) if isinstance(params["tuning"], list) else params["tuning"]
            cmd += ["-Tuning", tuning]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        return cmd
