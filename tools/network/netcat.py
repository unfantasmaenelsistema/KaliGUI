from tools.base import Tool, ToolField, FieldOption

_IP_PATTERN = r"[\w.\-]+"
_PORT_PATTERN = r"\d{1,5}"


class NetcatTool(Tool):
    name = "nc"
    description = "Navaja suiza de red: listeners, shells inversas, transferencia de ficheros"
    category = "network"
    icon = "🔗"
    fields = [
        ToolField("mode", "Modo", "select", required=True, default="connect",
                  options=[
                      FieldOption("connect — conectar a host:puerto", "connect"),
                      FieldOption("listen  — escuchar en un puerto (reverse shell)", "listen"),
                      FieldOption("scan    — escanear puertos (sin nmap)", "scan"),
                  ], group="Mode"),

        # Connect mode
        ToolField("host", "Host objetivo", "text",
                  placeholder="192.168.1.10",
                  pattern=_IP_PATTERN,
                  pattern_msg="Introduce una IP o hostname válido.",
                  help="Solo para modo connect y scan",
                  group="Target"),
        ToolField("port", "Puerto", "text", required=True,
                  placeholder="4444 o 1-1024 (scan)",
                  help="Puerto o rango para modo scan (ej: 1-1024)",
                  group="Target"),

        # Listen mode
        ToolField("listen_port", "Puerto de escucha", "number",
                  placeholder="4444",
                  min_val=1, max_val=65535,
                  help="Puerto donde escuchar (modo listen)",
                  group="Listen"),

        ToolField("udp", "Usar UDP en vez de TCP", "checkbox",
                  default=False, group="Options"),
        ToolField("verbose", "Verbose (-v)", "checkbox",
                  default=True, group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-e /bin/bash  (¡cuidado!)",
                  help="Flags extra para nc",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        mode = params.get("mode", "connect")
        cmd = ["nc"]

        if params.get("verbose"):
            cmd.append("-v")
        if params.get("udp"):
            cmd.append("-u")

        if mode == "listen":
            cmd += ["-l", "-p", str(params.get("listen_port", "4444"))]
        elif mode == "scan":
            cmd += ["-z"]
            if params.get("host"):
                cmd.append(params["host"])
            cmd.append(params.get("port", "1-1024"))
        else:  # connect
            if params.get("host"):
                cmd.append(params["host"])
            cmd.append(str(params.get("port", "")))

        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()

        return cmd
