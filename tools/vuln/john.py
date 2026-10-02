from tools.base import Tool, ToolField, FieldOption


class JohnTool(Tool):
    name = "john"
    description = "Cracking de hashes de contraseñas (John the Ripper)"
    category = "vuln"
    icon = "🔓"
    fields = [
        ToolField("hashfile", "Fichero de hashes", "text", required=True,
                  placeholder="/home/kali/hashes.txt",
                  help="Fichero con los hashes a crackear (formato john o /etc/shadow)",
                  group="Input"),
        ToolField("wordlist", "Wordlist", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Dejar vacío para usar el modo incremental",
                  group="Input"),
        ToolField("format", "Formato del hash", "select", default="",
                  options=[
                      FieldOption("— auto-detectar", ""),
                      FieldOption("md5crypt — Linux MD5 ($1$)", "md5crypt"),
                      FieldOption("sha512crypt — Linux SHA-512 ($6$)", "sha512crypt"),
                      FieldOption("sha256crypt — Linux SHA-256 ($5$)", "sha256crypt"),
                      FieldOption("bcrypt — bcrypt ($2a$, $2b$)", "bcrypt"),
                      FieldOption("NT — Windows NTLM", "NT"),
                      FieldOption("LM — Windows LM", "LM"),
                      FieldOption("raw-md5 — MD5 puro", "raw-md5"),
                      FieldOption("raw-sha1 — SHA1 puro", "raw-sha1"),
                      FieldOption("raw-sha256 — SHA256 puro", "raw-sha256"),
                      FieldOption("raw-sha512 — SHA512 puro", "raw-sha512"),
                      FieldOption("zip — ZIP password", "zip"),
                      FieldOption("rar — RAR password", "rar"),
                  ],
                  help="Si lo dejas vacío John intentará auto-detectar el formato",
                  group="Options"),
        ToolField("rules", "Reglas de mutación", "select", default="",
                  options=[
                      FieldOption("— ninguna", ""),
                      FieldOption("Wordlist — reglas básicas", "Wordlist"),
                      FieldOption("Best64 — 64 mejores reglas", "Best64"),
                      FieldOption("KoreLogic — reglas avanzadas", "KoreLogic"),
                      FieldOption("All — todas las reglas", "All"),
                  ],
                  help="Aplicar reglas de mutación a la wordlist",
                  group="Options"),
        ToolField("show", "Mostrar passwords crackeadas (--show)", "checkbox",
                  default=False,
                  help="Ver las contraseñas ya crackeadas en ejecuciones anteriores",
                  group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--min-length=6 --fork=4",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["john"]

        if params.get("wordlist"):
            cmd += [f"--wordlist={params['wordlist']}"]
        if params.get("format"):
            cmd += [f"--format={params['format']}"]
        if params.get("rules"):
            cmd += [f"--rules={params['rules']}"]
        if params.get("show"):
            cmd.append("--show")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()

        cmd.append(params["hashfile"])
        return cmd
