from tools.base import Tool, ToolField, FieldOption

_IP_PATTERN = r"[\w.\-]+"


class Enum4linuxTool(Tool):
    name = "enum4linux"
    description = "Enumeración SMB/Samba: usuarios, shares, grupos, políticas"
    category = "recon"
    icon = "🪟"
    fields = [
        ToolField("target", "IP / Hostname objetivo", "text", required=True,
                  placeholder="192.168.1.10",
                  pattern=_IP_PATTERN,
                  pattern_msg="Introduce una IP o hostname válido.",
                  group="Target"),
        ToolField("checks", "Checks a realizar", "multiselect",
                  options=[
                      FieldOption("U — usuarios del dominio", "U"),
                      FieldOption("S — shares disponibles", "S"),
                      FieldOption("G — grupos del dominio", "G"),
                      FieldOption("P — política de contraseñas", "P"),
                      FieldOption("r — usuarios via RID cycling", "r"),
                      FieldOption("o — información del OS", "o"),
                      FieldOption("i — información de impresoras", "i"),
                  ],
                  help="Dejar vacío para ejecutar todos los checks (-a)",
                  group="Options"),
        ToolField("username", "Usuario SMB", "text",
                  placeholder="guest o Administrator",
                  help="Dejar vacío para sesión nula (null session)",
                  group="Auth"),
        ToolField("password", "Contraseña SMB", "text",
                  placeholder="password123",
                  help="Dejar vacío para sesión nula",
                  group="Auth"),
        ToolField("rid_range", "Rango RID (para -r)", "text",
                  default="500-600",
                  placeholder="500-1000",
                  help="Rango de RIDs para enumerar usuarios",
                  group="Advanced"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-v",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["enum4linux"]

        checks = params.get("checks", [])
        if checks and isinstance(checks, list) and len(checks) > 0:
            for c in checks:
                cmd.append(f"-{c}")
        else:
            cmd.append("-a")

        if params.get("username"):
            cmd += ["-u", params["username"]]
        if params.get("password"):
            cmd += ["-p", params["password"]]
        if params.get("rid_range") and "r" in (params.get("checks") or []):
            cmd += ["-R", params["rid_range"]]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()

        cmd.append(params["target"])
        return cmd
