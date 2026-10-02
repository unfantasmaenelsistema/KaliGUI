#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════╗
# ║              KaliGUI — Script de instalación             ║
# ║         unfantasmaenelsistema.com                        ║
# ╚══════════════════════════════════════════════════════════╝

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✔${NC}  $*"; }
warn() { echo -e "  ${YELLOW}⚠${NC}  $*"; }
err()  { echo -e "  ${RED}✘${NC}  $*"; }
info() { echo -e "  ${BLUE}→${NC}  $*"; }
sep()  { echo -e "${CYAN}──────────────────────────────────────────────────${NC}"; }

clear
echo ""
echo -e "${BOLD}${GREEN}"
echo "  ██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██╗   ██╗██╗"
echo "  ██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██║   ██║██║"
echo "  █████╔╝ ███████║██║     ██║██║  ███╗██║   ██║██║"
echo "  ██╔═██╗ ██╔══██║██║     ██║██║   ██║██║   ██║██║"
echo "  ██║  ██╗██║  ██║███████╗██║╚██████╔╝╚██████╔╝██║"
echo "  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝  ╚═════╝ ╚═╝"
echo -e "${NC}"
echo -e "  ${CYAN}Interfaz web para herramientas de Kali Linux${NC}"
echo -e "  ${BLUE}unfantasmaenelsistema.com${NC}"
echo ""
sep

# ── 0. Root / sudo ─────────────────────────────────────────
SUDO=""
if [[ $EUID -ne 0 ]]; then
    if command -v sudo &>/dev/null; then
        SUDO="sudo"
        info "Ejecutando con sudo (se pedirá contraseña si es necesario)"
    else
        err "Este script necesita privilegios de root para instalar paquetes"
        exit 1
    fi
fi

# Directorio del script (ruta absoluta, sin symlinks)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. Sistema ──────────────────────────────────────────────
sep
echo -e "${BOLD}[1/5] Verificando sistema${NC}"
sep

if grep -qi "kali" /etc/os-release 2>/dev/null; then
    ok "Kali Linux detectado"
elif grep -qi "debian\|ubuntu\|parrot" /etc/os-release 2>/dev/null; then
    warn "No es Kali Linux pero es compatible (Debian/Ubuntu/Parrot)"
else
    warn "Sistema no reconocido — el script intentará continuar"
fi
info "Arquitectura: $(uname -m)"

# ── 2. Dependencias base ────────────────────────────────────
sep
echo -e "${BOLD}[2/5] Actualizando apt e instalando dependencias base${NC}"
sep

info "Actualizando lista de paquetes..."
$SUDO apt-get update -qq 2>/dev/null && ok "apt-get update completado" || warn "apt-get update falló (continuando)"

BASE_PKGS=(python3 python3-pip python3-venv curl git)
for pkg in "${BASE_PKGS[@]}"; do
    if dpkg -s "$pkg" &>/dev/null; then
        ok "$pkg ya instalado"
    else
        info "Instalando $pkg..."
        $SUDO apt-get install -y -qq "$pkg" && ok "$pkg instalado" || err "No se pudo instalar $pkg"
    fi
done

# ── 3. Entorno virtual Python ───────────────────────────────
sep
echo -e "${BOLD}[3/5] Configurando entorno Python${NC}"
sep

VENV_DIR="$SCRIPT_DIR/venv"

if [[ -d "$VENV_DIR" ]]; then
    ok "Entorno virtual ya existe en $VENV_DIR"
else
    info "Creando entorno virtual en $VENV_DIR..."
    python3 -m venv "$VENV_DIR" && ok "Entorno virtual creado"
fi

info "Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

info "Instalando dependencias Python (Flask, Flask-SocketIO)..."
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt" && ok "Dependencias Python instaladas"

# ── 4. Herramientas de Kali ─────────────────────────────────
sep
echo -e "${BOLD}[4/5] Verificando herramientas de Kali${NC}"
sep

# Herramientas instalables vía apt
declare -A TOOL_PACKAGES=(
    ["nmap"]="nmap"
    ["whatweb"]="whatweb"
    ["theHarvester"]="theharvester"
    ["gobuster"]="gobuster"
    ["enum4linux"]="enum4linux"
    ["nikto"]="nikto"
    ["sqlmap"]="sqlmap"
    ["wpscan"]="wpscan"
    ["john"]="john"
    ["hashcat"]="hashcat"
    ["msfconsole"]="metasploit-framework"
    ["hydra"]="hydra"
    ["nc"]="netcat-traditional"
    ["aircrack-ng"]="aircrack-ng"
    ["binwalk"]="binwalk"
)

# Herramientas que se instalan vía pip (no están en apt o el paquete difiere)
declare -A PIP_TOOLS=(
    ["volatility3"]="volatility3"
    ["crackmapexec"]="crackmapexec"
)

INSTALLED_APT=()
MISSING_APT=()
INSTALLED_PIP=()
MISSING_PIP=()

# Verificar herramientas apt
for tool in "${!TOOL_PACKAGES[@]}"; do
    if command -v "$tool" &>/dev/null; then
        INSTALLED_APT+=("$tool")
        ok "$tool"
    else
        MISSING_APT+=("$tool")
        warn "$tool — NO encontrado"
    fi
done

# Verificar herramientas pip
for tool in "${!PIP_TOOLS[@]}"; do
    if command -v "$tool" &>/dev/null; then
        INSTALLED_PIP+=("$tool")
        ok "$tool"
    else
        MISSING_PIP+=("$tool")
        warn "$tool — NO encontrado (requiere pip)"
    fi
done

TOTAL_INSTALLED=$(( ${#INSTALLED_APT[@]} + ${#INSTALLED_PIP[@]} ))
TOTAL_TOOLS=$(( ${#TOOL_PACKAGES[@]} + ${#PIP_TOOLS[@]} ))
echo ""
info "$TOTAL_INSTALLED de $TOTAL_TOOLS herramientas encontradas"

# Instalar herramientas apt que faltan
if [[ ${#MISSING_APT[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}  Faltan (apt): ${MISSING_APT[*]}${NC}"
    read -rp "  ¿Instalar automáticamente vía apt? [S/n] " APT_CHOICE
    APT_CHOICE="${APT_CHOICE:-S}"
    if [[ "$APT_CHOICE" =~ ^[Ss]$ ]]; then
        PKGS=()
        for tool in "${MISSING_APT[@]}"; do PKGS+=("${TOOL_PACKAGES[$tool]}"); done
        PKGS_UNIQUE=($(printf '%s\n' "${PKGS[@]}" | sort -u))
        info "Instalando: ${PKGS_UNIQUE[*]}"
        $SUDO apt-get install -y "${PKGS_UNIQUE[@]}" 2>/dev/null && ok "Herramientas apt instaladas" || {
            warn "Algunas no se instalaron. Prueba: sudo apt install ${PKGS_UNIQUE[*]}"
        }
    fi
fi

# Instalar herramientas pip que faltan
if [[ ${#MISSING_PIP[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}  Faltan (pip): ${MISSING_PIP[*]}${NC}"
    echo -e "  ${CYAN}Nota: crackmapexec y volatility3 se instalan vía pip${NC}"
    read -rp "  ¿Instalar vía pip? [S/n] " PIP_CHOICE
    PIP_CHOICE="${PIP_CHOICE:-S}"
    if [[ "$PIP_CHOICE" =~ ^[Ss]$ ]]; then
        for tool in "${MISSING_PIP[@]}"; do
            PKG="${PIP_TOOLS[$tool]}"
            info "pip install $PKG ..."
            # Instalar globalmente (fuera del venv) para que sea accesible como comando
            $SUDO pip3 install "$PKG" --break-system-packages 2>/dev/null \
                || pip3 install "$PKG" 2>/dev/null \
                || warn "No se pudo instalar $PKG — instálalo manualmente: pip3 install $PKG"
            command -v "$tool" &>/dev/null && ok "$tool instalado" || warn "$tool instalado pero no está en PATH — puede requerir reiniciar la terminal"
        done
    fi
fi

# ── 5. Wordlists ────────────────────────────────────────────
sep
echo -e "${BOLD}[5/5] Verificando wordlists${NC}"
sep

WORDLIST_DIR="/usr/share/wordlists"
ROCKYOU="$WORDLIST_DIR/rockyou.txt"
ROCKYOU_GZ="$WORDLIST_DIR/rockyou.txt.gz"

if [[ -f "$ROCKYOU" ]]; then
    SIZE=$(du -sh "$ROCKYOU" | cut -f1)
    ok "rockyou.txt disponible ($SIZE)"
elif [[ -f "$ROCKYOU_GZ" ]]; then
    warn "rockyou.txt está comprimido"
    read -rp "  ¿Descomprimir ahora? [S/n] " UNZIP_CHOICE
    UNZIP_CHOICE="${UNZIP_CHOICE:-S}"
    if [[ "$UNZIP_CHOICE" =~ ^[Ss]$ ]]; then
        $SUDO gunzip "$ROCKYOU_GZ" && ok "rockyou.txt descomprimido" || err "Error descomprimiendo"
    fi
else
    warn "rockyou.txt no encontrado en $WORDLIST_DIR"
fi

if [[ -d "/usr/share/seclists" ]]; then
    ok "SecLists disponible en /usr/share/seclists"
else
    warn "SecLists no encontrado"
    read -rp "  ¿Instalar SecLists? (~900MB) [s/N] " SECLISTS_CHOICE
    SECLISTS_CHOICE="${SECLISTS_CHOICE:-N}"
    if [[ "$SECLISTS_CHOICE" =~ ^[Ss]$ ]]; then
        $SUDO apt-get install -y -qq seclists && ok "SecLists instalado" || err "No se pudo instalar SecLists"
    fi
fi

# ── Crear start.sh ──────────────────────────────────────────
sep
echo -e "${BOLD}Creando script de arranque${NC}"
sep

LAUNCH_SCRIPT="$SCRIPT_DIR/start.sh"
cat > "$LAUNCH_SCRIPT" << LAUNCH
#!/usr/bin/env bash
# KaliGUI — Script de arranque
DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
source "\$DIR/venv/bin/activate"
cd "\$DIR"
export PYTHONPATH="\$DIR"
echo ""
echo "  KaliGUI iniciando..."
echo "  Accede en: http://localhost:5000"
echo "  (Ctrl+C para parar)"
echo ""
python3 "\$DIR/app.py"
LAUNCH
chmod +x "$LAUNCH_SCRIPT"
ok "Script de arranque creado: ./start.sh"

# Acceso directo en el escritorio
DESKTOP_DIR="$HOME/Desktop"
if [[ -d "$DESKTOP_DIR" ]]; then
    DESKTOP_FILE="$DESKTOP_DIR/KaliGUI.desktop"
    cat > "$DESKTOP_FILE" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=KaliGUI
Comment=Interfaz web para herramientas de Kali
Exec=bash -c "cd $SCRIPT_DIR && ./start.sh"
Icon=$SCRIPT_DIR/static/icon.png
Terminal=true
Categories=Security;Network;
DESKTOP
    chmod +x "$DESKTOP_FILE"
    ok "Acceso directo creado en el escritorio"
fi

# ── Resumen ─────────────────────────────────────────────────
sep
echo ""
echo -e "${BOLD}${GREEN}  ¡Instalación completada!${NC}"
echo ""
echo -e "  ${BOLD}Para arrancar KaliGUI:${NC}"
echo -e "  ${CYAN}  ./start.sh${NC}"
echo ""
echo -e "  ${BOLD}O manualmente:${NC}"
echo -e "  ${CYAN}  source venv/bin/activate${NC}"
echo -e "  ${CYAN}  cd $SCRIPT_DIR && python3 app.py${NC}"
echo ""
echo -e "  ${BOLD}Accede desde el navegador en:${NC}"
echo -e "  ${CYAN}  http://localhost:5000${NC}  (desde Kali)"
IFACE_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}')
if [[ -n "$IFACE_IP" ]]; then
    echo -e "  ${CYAN}  http://$IFACE_IP:5000${NC}  (desde tu host/red local)"
fi
echo ""
echo -e "  ${BLUE}unfantasmaenelsistema.com${NC}"
echo ""
sep
