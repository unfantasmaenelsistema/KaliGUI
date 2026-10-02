from tools.base import Tool, ToolField, FieldOption

_TARGET_PATTERN = r"[\w.\-/]+([\s,][\w.\-/]+)*"


class CrackMapExecTool(Tool):
    name = "crackmapexec"
    description = "Post-explotación y movimiento lateral en redes Windows/AD"
    category = "network"
    icon = "🗡️"
    fields = [
        ToolField("protocol", "Protocolo", "select", required=True, default="smb",
                  options=[
                      FieldOption("smb  — Windows/Samba", "smb"),
                      FieldOption("ssh  — SSH", "ssh"),
                      FieldOption("rdp  — Remote Desktop", "rdp"),
                      FieldOption("winrm — WinRM", "winrm"),
                      FieldOption("ldap — LDAP/AD", "ldap"),
                      FieldOption("mssql — SQL Server", "mssql"),
                      FieldOption("ftp  — FTP", "ftp"),
                  ], group="Target"),
        ToolField("target", "Target (IP / rango / fichero)", "text", required=True,
                  placeholder="192.168.1.0/24 o 192.168.1.10",
                  pattern=_TARGET_PATTERN,
                  pattern_msg="Introduce una IP, rango CIDR o lista de IPs.",
                  group="Target"),
        ToolField("username", "Usuario", "text",
                  placeholder="Administrator",
                  group="Auth"),
        ToolField("userlist", "Lista de usuarios", "text",
                  placeholder="/usr/share/wordlists/users.txt",
                  help="Alternativa a un solo usuario",
                  group="Auth"),
        ToolField("password", "Contraseña", "text",
                  placeholder="Password123",
                  group="Auth"),
        ToolField("passlist", "Lista de contraseñas", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Alternativa a una sola contraseña",
                  group="Auth"),
        ToolField("hash", "Hash NTLM (Pass-the-Hash)", "text",
                  placeholder="aad3b435b51404eeaad3b435b51404ee:31d6...",
                  help="Formato LM:NTLM o solo NTLM",
                  group="Auth"),
        ToolField("domain", "Dominio", "text",
                  placeholder="WORKGROUP o corp.local",
                  group="Auth"),
        ToolField("action", "Acción (módulo SMB)", "select", default="",
                  options=[
                      FieldOption("— ninguna (solo autenticación)", ""),
                      FieldOption("--shares — listar shares", "--shares"),
                      FieldOption("--sessions — sesiones activas", "--sessions"),
                      FieldOption("--disks — discos", "--disks"),
                      FieldOption("--users — usuarios del dominio", "--users"),
                      FieldOption("--groups — grupos del dominio", "--groups"),
                      FieldOption("--rid-brute — RID brute force", "--rid-brute"),
                      FieldOption("--sam — dump SAM (local admins)", "--sam"),
                      FieldOption("--lsa — dump LSA secrets", "--lsa"),
                  ],
                  help="Acción a ejecutar tras autenticarse (solo SMB)",
                  group="Actions"),
        ToolField("continue_on_success", "Continuar tras éxito (-d)", "checkbox",
                  default=True,
                  help="No parar al encontrar credenciales válidas",
                  group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--no-bruteforce --timeout 10",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["crackmapexec", params["protocol"], params["target"]]

        if params.get("username"):
            cmd += ["-u", params["username"]]
        elif params.get("userlist"):
            cmd += ["-u", params["userlist"]]

        if params.get("hash"):
            cmd += ["-H", params["hash"]]
        elif params.get("password"):
            cmd += ["-p", params["password"]]
        elif params.get("passlist"):
            cmd += ["-p", params["passlist"]]

        if params.get("domain"):
            cmd += ["-d", params["domain"]]

        if params.get("action"):
            cmd.append(params["action"])

        if params.get("continue_on_success"):
            cmd.append("--continue-on-success")

        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()

        return cmd
