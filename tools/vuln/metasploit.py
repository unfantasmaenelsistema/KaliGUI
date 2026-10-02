from tools.base import Tool, ToolField, FieldOption

_IP_PATTERN = r"[\w.\-]+"


class MetasploitTool(Tool):
    name = "msfconsole"
    description = "Lanzar módulos de Metasploit Framework directamente"
    category = "vuln"
    icon = "☠️"
    fields = [
        ToolField("module", "Módulo", "text", required=True,
                  placeholder="exploit/multi/handler o auxiliary/scanner/smb/smb_ms17_010",
                  help="Ruta completa del módulo Metasploit",
                  group="Module"),
        ToolField("rhosts", "RHOSTS (objetivo/s)", "text",
                  placeholder="192.168.1.10 o 192.168.1.0/24",
                  pattern=_IP_PATTERN,
                  pattern_msg="Introduce una IP o rango válido.",
                  group="Options"),
        ToolField("rport", "RPORT", "number",
                  placeholder="445",
                  min_val=1, max_val=65535,
                  group="Options"),
        ToolField("lhost", "LHOST (tu IP)", "text",
                  placeholder="192.168.1.5",
                  help="Tu IP para recibir la reverse shell",
                  group="Options"),
        ToolField("lport", "LPORT (tu puerto)", "number",
                  placeholder="4444",
                  min_val=1, max_val=65535,
                  group="Options"),
        ToolField("payload", "Payload", "text",
                  placeholder="windows/x64/meterpreter/reverse_tcp",
                  help="Dejar vacío para usar el payload por defecto del módulo",
                  group="Payload"),
        ToolField("extra_opts", "Opciones adicionales", "textarea",
                  placeholder="set SMBUser admin\nset SMBPass password123",
                  help="Una opción por línea en formato: set OPCION valor",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        # Build a msfconsole -x "commands" invocation
        cmds = [f"use {params['module']}"]

        if params.get("rhosts"):
            cmds.append(f"set RHOSTS {params['rhosts']}")
        if params.get("rport"):
            cmds.append(f"set RPORT {params['rport']}")
        if params.get("lhost"):
            cmds.append(f"set LHOST {params['lhost']}")
        if params.get("lport"):
            cmds.append(f"set LPORT {params['lport']}")
        if params.get("payload"):
            cmds.append(f"set PAYLOAD {params['payload']}")

        # Extra options: one per line
        if params.get("extra_opts"):
            for line in params["extra_opts"].splitlines():
                line = line.strip()
                if line:
                    cmds.append(line)

        cmds.append("run")

        return ["msfconsole", "-q", "-x", "; ".join(cmds)]
