from tools.base import Tool, ToolField, FieldOption

# Regex: IP, hostname, CIDR range, or range like 192.168.1.1-20
_TARGET_PATTERN = r"[\w.\-/]+([\s,][\w.\-/]+)*"

class NmapTool(Tool):
    name = "nmap"
    description = "Escáner de puertos y detección de servicios/OS"
    category = "recon"
    icon = "🗺️"
    fields = [
        ToolField("target", "Target (IP / rango / hostname)", "text", required=True,
                  placeholder="192.168.1.0/24",
                  help="Acepta IPs, rangos CIDR o hostnames",
                  pattern=_TARGET_PATTERN,
                  pattern_msg="Target inválido. Ejemplos: 192.168.1.1, 192.168.1.0/24, host.local",
                  group="Target"),
        ToolField("scan_type", "Tipo de escaneo", "select", default="-sV",
                  options=[
                      FieldOption("SYN Stealth (-sS)", "-sS"),
                      FieldOption("Version Detection (-sV)", "-sV"),
                      FieldOption("OS Detection (-O)", "-O"),
                      FieldOption("Aggressive (-A)", "-A"),
                      FieldOption("UDP (-sU)", "-sU"),
                      FieldOption("Ping scan (-sn)", "-sn"),
                  ], group="Scan"),
        ToolField("ports", "Puertos", "text",
                  placeholder="22,80,443 o 1-1000 o vacío = default",
                  pattern=r"(\d+(-\d+)?(,\d+(-\d+)?)*)?",
                  pattern_msg="Formato de puertos inválido. Ejemplos: 80, 22,80,443, 1-1000",
                  help="Dejar vacío para usar los 1000 más comunes", group="Scan"),
        ToolField("timing", "Velocidad (timing)", "select", default="-T3",
                  options=[
                      FieldOption("T0 - Paranoid (IDS evasion)", "-T0"),
                      FieldOption("T1 - Sneaky", "-T1"),
                      FieldOption("T2 - Polite", "-T2"),
                      FieldOption("T3 - Normal", "-T3"),
                      FieldOption("T4 - Aggressive", "-T4"),
                      FieldOption("T5 - Insane", "-T5"),
                  ], group="Scan"),
        ToolField("scripts", "NSE Scripts", "text",
                  placeholder="vuln, http-enum, smb-vuln-*",
                  help="Scripts NSE separados por coma", group="Advanced"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-Pn --open -v",
                  help="Cualquier flag extra de nmap", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["nmap"]
        cmd.append(params["scan_type"])
        cmd.append(params["timing"])
        if params.get("ports"):
            cmd += ["-p", params["ports"]]
        if params.get("scripts"):
            cmd += ["--script", params["scripts"]]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        cmd.append(params["target"])
        return cmd
