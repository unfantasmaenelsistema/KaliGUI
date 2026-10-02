from tools.base import Tool, ToolField, FieldOption

_URL_PATTERN = r"https?://[\w.\-]+(:\d+)?(/[\w.\-/?=&%#]*)?"

class WhatWebTool(Tool):
    name = "whatweb"
    description = "Fingerprinting de tecnologías web (CMS, frameworks, servidores)"
    category = "recon"
    icon = "🌐"
    fields = [
        ToolField("target", "URL objetivo", "text", required=True,
                  placeholder="http://192.168.1.10",
                  pattern=_URL_PATTERN,
                  pattern_msg="Introduce una URL válida. Ejemplo: http://192.168.1.10 o https://example.com",
                  group="Target"),
        ToolField("aggression", "Nivel de agresividad", "select", default="1",
                  options=[
                      FieldOption("1 - Pasivo (una petición)", "1"),
                      FieldOption("3 - Agresivo (más peticiones)", "3"),
                      FieldOption("4 - Heavy (máximas peticiones)", "4"),
                  ], group="Options"),
        ToolField("follow_redirect", "Seguir redirecciones", "checkbox", default=True, group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text", placeholder="--no-errors",
                  help="Flags extra de whatweb", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["whatweb"]
        cmd += ["-a", params.get("aggression", "1")]
        if params.get("follow_redirect"):
            cmd.append("--follow-redirect=always")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        cmd.append(params["target"])
        return cmd
