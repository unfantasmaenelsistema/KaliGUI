from tools.base import Tool, ToolField, FieldOption


class BinwalkTool(Tool):
    name = "binwalk"
    description = "Análisis y extracción de firmwares y ficheros binarios"
    category = "forensics"
    icon = "🔩"
    fields = [
        ToolField("file", "Fichero a analizar", "text", required=True,
                  placeholder="/home/kali/firmware.bin", group="Input"),
        ToolField("extract", "Extraer ficheros embebidos (-e)", "checkbox", default=False,
                  group="Options"),
        ToolField("signature", "Mostrar firmas conocidas (-B)", "checkbox", default=True,
                  group="Options"),
        ToolField("strings", "Buscar strings imprimibles (-S)", "checkbox", default=False,
                  group="Options"),
        ToolField("entropy", "Análisis de entropía (-E)", "checkbox", default=False,
                  help="Detecta zonas cifradas o comprimidas", group="Options"),
        ToolField("extra_flags", "Flags adicionales", "text",
                  placeholder="--dd='zip:zip'", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["binwalk"]
        if params.get("signature"):
            cmd.append("-B")
        if params.get("extract"):
            cmd.append("-e")
        if params.get("strings"):
            cmd.append("-S")
        if params.get("entropy"):
            cmd.append("-E")
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        cmd.append(params["file"])
        return cmd
