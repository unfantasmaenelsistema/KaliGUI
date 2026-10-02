from tools.base import Tool, ToolField, FieldOption

_DOMAIN_PATTERN = r"[\w][\w.\-]*\.[a-zA-Z]{2,}"

class TheHarvesterTool(Tool):
    name = "theHarvester"
    description = "OSINT: emails, subdominios, IPs y URLs desde fuentes públicas"
    category = "recon"
    icon = "🌾"
    fields = [
        ToolField("domain", "Dominio objetivo", "text", required=True,
                  placeholder="ejemplo.com",
                  pattern=_DOMAIN_PATTERN,
                  pattern_msg="Introduce un dominio válido. Ejemplo: ejemplo.com",
                  group="Target"),
        ToolField("source", "Fuente de datos", "select", default="all",
                  options=[
                      FieldOption("Todas", "all"),
                      FieldOption("Google", "google"),
                      FieldOption("Bing", "bing"),
                      FieldOption("DuckDuckGo", "duckduckgo"),
                      FieldOption("LinkedIn", "linkedin"),
                      FieldOption("Shodan", "shodan"),
                      FieldOption("CertSpotter", "certspotter"),
                      FieldOption("HackerTarget", "hackertarget"),
                  ], group="Options"),
        ToolField("limit", "Límite de resultados", "number", default=200,
                  placeholder="200",
                  min_val=1, max_val=10000,
                  group="Options"),
        ToolField("dns_brute", "Brute-force DNS", "checkbox", default=False,
                  help="Activa fuerza bruta de subdominios", group="Options"),
    ]

    def build_command(self, params: dict) -> list[str]:
        cmd = ["theHarvester", "-d", params["domain"],
               "-b", params.get("source", "all"),
               "-l", str(params.get("limit", 200))]
        if params.get("dns_brute"):
            cmd.append("-c")
        return cmd
