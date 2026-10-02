from tools.base import Tool, ToolField, FieldOption


class AircrackTool(Tool):
    name = "aircrack-ng"
    description = "Cracking de claves WEP/WPA/WPA2 a partir de capturas .cap"
    category = "network"
    icon = "📡"
    fields = [
        ToolField("capfile", "Fichero de captura (.cap / .ivs)", "text", required=True,
                  placeholder="/home/kali/capture.cap",
                  help="Ruta al fichero de captura con el handshake", group="Input"),
        ToolField("wordlist", "Wordlist (WPA/WPA2)", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Solo necesaria para WPA/WPA2", group="Input"),
        ToolField("bssid", "BSSID del AP objetivo", "text",
                  placeholder="AA:BB:CC:DD:EE:FF",
                  help="MAC del access point (filtra si hay múltiples en la captura)", group="Options"),
        ToolField("essid", "ESSID (nombre de red)", "text",
                  placeholder="NombreDeRed",
                  help="Nombre de la red WiFi objetivo", group="Options"),
        ToolField("wep", "Modo WEP", "checkbox", default=False,
                  help="Activar para redes WEP (no requiere wordlist)", group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-n 128", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["aircrack-ng"]
        if params.get("bssid"):
            cmd += ["-b", params["bssid"]]
        if params.get("essid"):
            cmd += ["-e", params["essid"]]
        if params.get("wordlist") and not params.get("wep"):
            cmd += ["-w", params["wordlist"]]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        cmd.append(params["capfile"])
        return cmd
