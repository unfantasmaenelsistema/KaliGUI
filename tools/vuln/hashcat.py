from tools.base import Tool, ToolField, FieldOption


class HashcatTool(Tool):
    name = "hashcat"
    description = "Cracking de hashes acelerado por GPU (el más rápido)"
    category = "vuln"
    icon = "⚡"
    fields = [
        ToolField("hashfile", "Fichero de hashes / hash directo", "text", required=True,
                  placeholder="/home/kali/hashes.txt  o  5f4dcc3b5aa765d61d8327deb882cf99",
                  help="Ruta al fichero o el hash directamente",
                  group="Input"),
        ToolField("hash_type", "Tipo de hash (-m)", "select", required=True, default="0",
                  options=[
                      FieldOption("0    — MD5", "0"),
                      FieldOption("100  — SHA1", "100"),
                      FieldOption("1400 — SHA-256", "1400"),
                      FieldOption("1700 — SHA-512", "1700"),
                      FieldOption("900  — MD4", "900"),
                      FieldOption("1000 — NTLM", "1000"),
                      FieldOption("3000 — LM", "3000"),
                      FieldOption("5600 — NetNTLMv2", "5600"),
                      FieldOption("13100 — Kerberos 5 TGS-REP etype 23", "13100"),
                      FieldOption("1800 — sha512crypt $6$ (Linux)", "1800"),
                      FieldOption("500  — md5crypt $1$ (Linux)", "500"),
                      FieldOption("3200 — bcrypt $2*$", "3200"),
                      FieldOption("2500 — WPA/WPA2", "2500"),
                      FieldOption("13400 — KeePass", "13400"),
                      FieldOption("11600 — 7-Zip", "11600"),
                  ],
                  group="Options"),
        ToolField("attack_mode", "Modo de ataque (-a)", "select", default="0",
                  options=[
                      FieldOption("0 — Diccionario (wordlist)", "0"),
                      FieldOption("1 — Combinación (wordlist + wordlist)", "1"),
                      FieldOption("3 — Fuerza bruta / máscara", "3"),
                      FieldOption("6 — Diccionario + máscara", "6"),
                      FieldOption("7 — Máscara + diccionario", "7"),
                  ], group="Options"),
        ToolField("wordlist", "Wordlist", "text",
                  placeholder="/usr/share/wordlists/rockyou.txt",
                  help="Para modos 0, 1, 6 y 7",
                  group="Input"),
        ToolField("mask", "Máscara (para modo 3/6/7)", "text",
                  placeholder="?a?a?a?a?a?a  o  Pass?d?d?d",
                  help="?l=min, ?u=may, ?d=dígito, ?s=símbolo, ?a=todos",
                  group="Input"),
        ToolField("rules", "Fichero de reglas", "text",
                  placeholder="/usr/share/hashcat/rules/best64.rule",
                  help="Para modo diccionario con mutaciones",
                  group="Options"),
        ToolField("outfile", "Guardar resultados en", "text",
                  placeholder="/home/kali/cracked.txt",
                  group="Options"),
        ToolField("force", "Forzar ejecución (--force)", "checkbox",
                  default=False,
                  help="Ignorar advertencias (útil en VM sin GPU real)",
                  group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="-w 3 --status --status-timer 10",
                  group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["hashcat"]
        cmd += ["-m", params.get("hash_type", "0")]
        cmd += ["-a", params.get("attack_mode", "0")]
        cmd.append(params["hashfile"])

        if params.get("wordlist"):
            cmd.append(params["wordlist"])
        if params.get("mask"):
            cmd.append(params["mask"])
        if params.get("rules"):
            cmd += ["-r", params["rules"]]
        if params.get("outfile"):
            cmd += ["-o", params["outfile"]]
        if params.get("force"):
            cmd.append("--force")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()

        return cmd
