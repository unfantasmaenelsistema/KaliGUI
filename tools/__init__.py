# Recon
from tools.recon.nmap import NmapTool
from tools.recon.whatweb import WhatWebTool
from tools.recon.theharvester import TheHarvesterTool
from tools.recon.gobuster import GobusterTool
from tools.recon.enum4linux import Enum4linuxTool

# Vuln
from tools.vuln.nikto import NiktoTool
from tools.vuln.sqlmap import SqlmapTool
from tools.vuln.wpscan import WPScanTool
from tools.vuln.john import JohnTool
from tools.vuln.hashcat import HashcatTool
from tools.vuln.metasploit import MetasploitTool

# Network / Ataques
from tools.network.hydra import HydraTool
from tools.network.aircrack import AircrackTool
from tools.network.crackmapexec import CrackMapExecTool
from tools.network.netcat import NetcatTool

# Forensics
from tools.forensics.binwalk import BinwalkTool
from tools.forensics.volatility import VolatilityTool

TOOLS: dict = {}

def register(tool_class):
    instance = tool_class()
    TOOLS[instance.name] = instance

# Recon
register(NmapTool)
register(WhatWebTool)
register(TheHarvesterTool)
register(GobusterTool)
register(Enum4linuxTool)

# Vuln
register(NiktoTool)
register(SqlmapTool)
register(WPScanTool)
register(JohnTool)
register(HashcatTool)
register(MetasploitTool)

# Network
register(HydraTool)
register(CrackMapExecTool)
register(NetcatTool)
register(AircrackTool)

# Forensics
register(BinwalkTool)
register(VolatilityTool)

CATEGORIES = {
    "recon":     {"label": "Reconocimiento", "icon": "🔍"},
    "vuln":      {"label": "Vulnerabilidades", "icon": "🛡️"},
    "network":   {"label": "Ataques de Red", "icon": "📡"},
    "forensics": {"label": "Forense", "icon": "🔬"},
}
