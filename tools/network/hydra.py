from tools.base import Tool, ToolField, FieldOption


class HydraTool(Tool):
    name = "hydra"
    description = "Fuerza bruta de credenciales en múltiples protocolos"
    category = "network"
    icon = "🔑"
    fields = [
        ToolField("target", "IP / Hostname objetivo", "text", required=True,
                  placeholder="192.168.1.10", group="Target"),
        ToolField("service", "Servicio / Protocolo", "select", required=True,
                  options=[
                      FieldOption("SSH", "ssh"),
                      FieldOption("FTP", "ftp"),
                      FieldOption("HTTP GET", "http-get"),
                      FieldOption("HTTP POST", "http-post-form"),
                      FieldOption("SMB", "smb"),
                      FieldOption("RDP", "rdp"),
                      FieldOption("Telnet", "telnet"),
                      FieldOption("MySQL", "mysql"),
                      FieldOption("PostgreSQL", "postgres"),
                      FieldOption("VNC", "vnc"),
                  ], group="Target"),
        ToolField("port", "Puerto (opcional)", "number",
                  help="Dejar vacío para usar el puerto por defecto del servicio", group="Target"),
        ToolField("username", "Usuario", "text", placeholder="admin",
                  help="Un usuario concreto", group="Credentials"),
        ToolField("userlist", "Lista de usuarios", "text",
                  placeholder="/usr/share/wordlists/users.txt",
                  help="Ruta a fichero de usuarios (alternativa a un solo usuario)", group="Credentials"),
        ToolField("password", "Contraseña", "text", placeholder="password123",
                  help="Una contraseña concreta", group="Credentials"),
        ToolField("passlist", "Lista de contraseñas", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Ruta a wordlist (alternativa a una sola contraseña)", group="Credentials"),
        ToolField("threads", "Threads paralelos", "number", default=16,
                  help="Conexiones simultáneas (4-64 recomendado)", group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-V -f", help="-V verbose, -f parar al encontrar", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["hydra"]
        if params.get("username"):
            cmd += ["-l", params["username"]]
        elif params.get("userlist"):
            cmd += ["-L", params["userlist"]]
        if params.get("password"):
            cmd += ["-p", params["password"]]
        elif params.get("passlist"):
            cmd += ["-P", params["passlist"]]
        cmd += ["-t", str(params.get("threads", 16))]
        if params.get("port"):
            cmd += ["-s", str(params["port"])]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        cmd.append(params["target"])
        cmd.append(params["service"])
        return cmd
