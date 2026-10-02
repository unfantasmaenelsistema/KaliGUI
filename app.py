import os
import sys

# Ensure the project root is in the Python path regardless of how the script is launched
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import uuid
import json
import threading
import subprocess
from datetime import datetime
from flask import Flask, render_template, jsonify, request, make_response
from flask_socketio import SocketIO, emit

from tools import TOOLS, CATEGORIES
from cheatsheets import CHEATSHEETS

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

WORDLIST_DIRS = [
    "/usr/share/wordlists",
    "/usr/share/seclists",
    "/opt/wordlists",
]

active_processes: dict = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tools")
def api_tools():
    result = {}
    for cat_id, cat_info in CATEGORIES.items():
        result[cat_id] = {
            **cat_info,
            "tools": [t.to_dict() for t in TOOLS.values() if t.category == cat_id],
        }
    return jsonify(result)


@app.route("/api/sessions")
def api_sessions():
    sessions = []
    for fname in sorted(os.listdir(SESSIONS_DIR), reverse=True):
        if fname.endswith(".json"):
            path = os.path.join(SESSIONS_DIR, fname)
            try:
                with open(path) as f:
                    sessions.append(json.load(f))
            except Exception:
                pass
    return jsonify(sessions[:50])


@app.route("/api/sessions/<session_id>")
def api_session_detail(session_id):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    with open(path) as f:
        return jsonify(json.load(f))


@app.route("/api/sessions/<session_id>/export/<fmt>")
def api_export(session_id, fmt):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    with open(path) as f:
        s = json.load(f)

    if fmt == "txt":
        lines = [
            f"KaliGUI - Sesion {s['id']}",
            f"Herramienta : {s['tool']}",
            f"Comando     : {s['command']}",
            f"Inicio      : {s['started_at']}",
            f"Fin         : {s.get('finished_at', '-')}",
            f"Codigo      : {s.get('return_code', '-')}",
            "=" * 60,
            "",
        ] + s.get("output", [])
        content = "\n".join(lines)
        resp = make_response(content)
        resp.headers["Content-Type"] = "text/plain; charset=utf-8"
        resp.headers["Content-Disposition"] = f"attachment; filename=kaligui_{session_id}.txt"
        return resp

    elif fmt == "html":
        ok = s.get("return_code") == 0
        status_color = "#3fb950" if ok else "#ff7b72"
        status_text = "Completado" if ok else "Error"
        output_html = "\n".join(
            '<div class="line">' + line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") + '</div>'
            for line in s.get("output", [])
        )
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>KaliGUI - {s['tool']} #{s['id']}</title>
<style>
  body {{ background:#090c10; color:#c9d1d9; font-family:'Courier New',monospace; padding:30px; margin:0; }}
  h1 {{ color:#00ff88; font-size:20px; letter-spacing:3px; margin-bottom:6px; }}
  .meta {{ color:#8b949e; font-size:12px; margin-bottom:20px; line-height:2; }}
  .meta span {{ color:#c9d1d9; }}
  .status {{ color:{status_color}; font-weight:bold; }}
  .cmd {{ background:#161b22; border:1px solid #21262d; padding:10px 14px; border-radius:4px; color:#58a6ff; margin-bottom:20px; word-break:break-all; font-size:13px; }}
  .output {{ background:#0d1117; border:1px solid #21262d; border-radius:4px; padding:16px; }}
  .line {{ white-space:pre-wrap; word-break:break-all; font-size:12px; line-height:1.7; }}
  .footer {{ margin-top:20px; color:#484f58; font-size:11px; text-align:center; }}
  a {{ color:#00ff88; }}
</style>
</head>
<body>
<h1>KaliGUI - {s['tool'].upper()}</h1>
<div class="meta">
  Sesion <span>#{s['id']}</span><br>
  Inicio <span>{s['started_at']}</span><br>
  Fin <span>{s.get('finished_at','?')}</span><br>
  Estado <span class="status">{status_text} (codigo {s.get('return_code','?')})</span>
</div>
<div class="cmd">$ {s['command']}</div>
<div class="output">{output_html}</div>
<div class="footer">
  Generado por KaliGUI &nbsp;&middot;&nbsp;
  <a href="https://www.unfantasmaenelsistema.com" target="_blank">unfantasmaenelsistema.com</a>
</div>
</body>
</html>"""
        resp = make_response(html)
        resp.headers["Content-Type"] = "text/html; charset=utf-8"
        resp.headers["Content-Disposition"] = f"attachment; filename=kaligui_{session_id}.html"
        return resp

    return jsonify({"error": "formato no soportado"}), 400



@app.route("/api/preview", methods=["POST"])
def api_preview():
    """Return the exact command that would be executed, without running it."""
    data = request.get_json() or {}
    tool_name = data.get("tool")
    params = data.get("params", {})

    if tool_name not in TOOLS:
        return jsonify({"command": "herramienta desconocida"}), 404

    tool = TOOLS[tool_name]
    try:
        cmd = tool.build_command(params)
        return jsonify({"command": " ".join(cmd)})
    except Exception as e:
        return jsonify({"command": f"(error: {e})"}), 200




@app.route("/api/sessions/<session_id>/notes", methods=["GET", "POST"])
def api_session_notes(session_id):
    """Get or save notes for a session."""
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    with open(path) as f:
        session = json.load(f)
    if request.method == "POST":
        data = request.get_json() or {}
        session["notes"] = data.get("notes", "")
        with open(path, "w") as f:
            json.dump(session, f, indent=2, ensure_ascii=False)
        return jsonify({"ok": True})
    return jsonify({"notes": session.get("notes", "")})


@app.route("/api/running")
def api_running():
    """Return currently running processes."""
    running = []
    for session_id, proc in active_processes.items():
        # Try to find session info
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        tool = "?"
        command = "?"
        started_at = "?"
        if os.path.exists(path):
            try:
                with open(path) as f:
                    s = json.load(f)
                tool = s.get("tool", "?")
                command = s.get("command", "?")
                started_at = s.get("started_at", "?")
            except Exception:
                pass
        running.append({
            "session_id": session_id,
            "tool": tool,
            "command": command,
            "started_at": started_at,
            "pid": proc.pid if proc else None,
        })
    return jsonify(running)

@app.route("/api/dashboard")
def api_dashboard():
    """Return stats for the dashboard."""
    import collections
    sessions = []
    for fname in sorted(os.listdir(SESSIONS_DIR), reverse=True):
        if fname.endswith(".json"):
            path = os.path.join(SESSIONS_DIR, fname)
            try:
                with open(path) as f:
                    sessions.append(json.load(f))
            except Exception:
                pass

    total = len(sessions)
    success = sum(1 for s in sessions if s.get("return_code") == 0)
    failed  = sum(1 for s in sessions if s.get("return_code") not in (0, None))
    running = len(active_processes)

    # Most used tools
    tool_counts = collections.Counter(s.get("tool") for s in sessions)
    top_tools = [{"tool": t, "count": c} for t, c in tool_counts.most_common(5)]

    # Category counts
    cat_counts = collections.Counter(s.get("category") for s in sessions if s.get("category"))
    top_cats = [{"category": c, "count": n} for c, n in cat_counts.most_common()]

    # Recent sessions (last 5)
    recent = sessions[:5]

    # Tools available
    tools_available = len(TOOLS)

    return jsonify({
        "total_sessions": total,
        "success": success,
        "failed": failed,
        "running": running,
        "top_tools": top_tools,
        "top_cats": top_cats,
        "recent": recent,
        "tools_available": tools_available,
    })

@app.route("/api/cheatsheet/<tool_name>")
def api_cheatsheet(tool_name):
    """Return cheatsheet examples for a tool."""
    return jsonify(CHEATSHEETS.get(tool_name, []))

@app.route("/api/wordlists")
def api_wordlists():
    def scan_dir(path, depth=0):
        if depth > 3:
            return []
        items = []
        try:
            entries = sorted(os.scandir(path), key=lambda e: (e.is_file(), e.name.lower()))
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    children = scan_dir(entry.path, depth + 1)
                    if children:
                        items.append({"type": "dir", "name": entry.name, "path": entry.path, "children": children})
                elif entry.is_file() and entry.name.lower().endswith((".txt", ".lst", ".list", ".dic", ".dict")):
                    try:
                        size = entry.stat().st_size
                    except OSError:
                        size = 0
                    items.append({"type": "file", "name": entry.name, "path": entry.path, "size": size})
        except PermissionError:
            pass
        return items

    result = []
    for d in WORDLIST_DIRS:
        if os.path.isdir(d):
            children = scan_dir(d)
            if children:
                result.append({"type": "dir", "name": os.path.basename(d), "path": d, "children": children})
    return jsonify(result)


@socketio.on("run_tool")
def handle_run_tool(data):
    tool_name = data.get("tool")
    params = data.get("params", {})
    sid = request.sid

    if tool_name not in TOOLS:
        emit("error", {"message": f"Herramienta desconocida: {tool_name}"})
        return

    tool = TOOLS[tool_name]

    errors = tool.validate(params)
    if errors:
        emit("validation_errors", {"errors": errors})
        return

    try:
        cmd = tool.build_command(params)
    except Exception as e:
        emit("error", {"message": f"Error construyendo comando: {e}"})
        return

    session_id = str(uuid.uuid4())[:8]
    session = {
        "id": session_id,
        "tool": tool_name,
        "category": tool.category,
        "command": " ".join(cmd),
        "params": params,
        "started_at": datetime.now().isoformat(),
        "finished_at": None,
        "return_code": None,
        "output": [],
    }

    emit("session_start", {
        "session_id": session_id,
        "command": session["command"],
        "tool": tool_name,
    })

    def run():
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            active_processes[session_id] = process
            for line in iter(process.stdout.readline, ""):
                line = line.rstrip("\n")
                session["output"].append(line)
                socketio.emit("output", {"session_id": session_id, "line": line}, to=sid)
            process.wait()
            session["return_code"] = process.returncode
        except FileNotFoundError:
            msg = f"[ERROR] Herramienta no encontrada: '{cmd[0]}'. Esta instalada en Kali?"
            session["output"].append(msg)
            session["return_code"] = -1
            socketio.emit("output", {"session_id": session_id, "line": msg}, to=sid)
        except Exception as e:
            msg = f"[ERROR] {e}"
            session["output"].append(msg)
            session["return_code"] = -1
            socketio.emit("output", {"session_id": session_id, "line": msg}, to=sid)
        finally:
            active_processes.pop(session_id, None)
            session["finished_at"] = datetime.now().isoformat()
            path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
            with open(path, "w") as f:
                json.dump(session, f, indent=2, ensure_ascii=False)
            socketio.emit("session_done", {
                "session_id": session_id,
                "return_code": session["return_code"],
                "lines": len(session["output"]),
            }, to=sid)

    threading.Thread(target=run, daemon=True).start()


@socketio.on("kill_tool")
def handle_kill(data):
    session_id = data.get("session_id")
    proc = active_processes.get(session_id)
    if proc:
        proc.terminate()
        emit("output", {"session_id": session_id, "line": "[!] Proceso terminado por el usuario."})
    else:
        emit("error", {"message": "No hay proceso activo con ese ID"})


if __name__ == "__main__":
    print("KaliGUI iniciando en http://0.0.0.0:5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
