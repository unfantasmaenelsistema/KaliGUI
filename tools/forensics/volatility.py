from tools.base import Tool, ToolField, FieldOption


class VolatilityTool(Tool):
    name = "volatility3"
    description = "Análisis forense de volcados de memoria RAM"
    category = "forensics"
    icon = "🧠"
    fields = [
        ToolField("memdump", "Fichero de volcado de memoria", "text", required=True,
                  placeholder="/home/kali/memory.dmp", group="Input"),
        ToolField("plugin", "Plugin a ejecutar", "select", required=True,
                  options=[
                      FieldOption("windows.info — Info general del sistema", "windows.info"),
                      FieldOption("windows.pslist — Lista de procesos", "windows.pslist"),
                      FieldOption("windows.pstree — Árbol de procesos", "windows.pstree"),
                      FieldOption("windows.psscan — Escaneo de procesos ocultos", "windows.psscan"),
                      FieldOption("windows.cmdline — Argumentos de procesos", "windows.cmdline"),
                      FieldOption("windows.netscan — Conexiones de red", "windows.netscan"),
                      FieldOption("windows.netstat — Estado de red", "windows.netstat"),
                      FieldOption("windows.dlllist — DLLs cargadas", "windows.dlllist"),
                      FieldOption("windows.hashdump — Hashes de contraseñas", "windows.hashdump"),
                      FieldOption("windows.malfind — Procesos maliciosos", "windows.malfind"),
                      FieldOption("windows.filescan — Ficheros en memoria", "windows.filescan"),
                      FieldOption("windows.registry.hivelist — Hives del registro", "windows.registry.hivelist"),
                      FieldOption("linux.pslist — Lista de procesos (Linux)", "linux.pslist"),
                      FieldOption("linux.bash — Historial de bash", "linux.bash"),
                  ], group="Plugin"),
        ToolField("extra_flags", "Flags adicionales / filtros", "text",
                  placeholder="--pid 1234", group="Advanced"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["volatility3", "-f", params["memdump"], params["plugin"]]
        if params.get("extra_flags"):
            cmd += params["extra_flags"].split()
        return cmd
