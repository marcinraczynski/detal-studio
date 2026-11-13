"""Ustala dane FTP z sekretów FTP_* albo ze zbiorczego sekretu DETAL.

Nie wypisuje wartości. Rozpoznaje w DETAL: JSON, linie "nazwa: wartość"
lub "nazwa=wartość", a w ostateczności same wartości w osobnych liniach.
"""
import json, os, re, sys

KEYS = {
    "server": ("server", "serwer", "host", "adres"),
    "username": ("user", "login", "użytkownik", "uzytkownik", "nazwa"),
    "password": ("pass", "hasło", "haslo", "pwd"),
    "dir": ("dir", "katalog", "folder", "path", "ścieżka", "sciezka"),
}
HOST = re.compile(r"^(?:s?ftps?://)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)/?$", re.I)


def clean(v):
    return str(v).strip().strip("\"'`").strip()


def classify(label):
    label = label.lower()
    for field, words in KEYS.items():
        if any(w in label for w in words):
            return field
    return None


def parse(raw):
    out = {}
    raw = raw.strip()
    if not raw:
        return out
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            for k, v in data.items():
                f = classify(str(k))
                if f and f not in out:
                    out[f] = clean(v)
            return out
    except ValueError:
        pass
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if len(lines) == 1:
        lines = [p for p in re.split(r"\s*[;,]\s*|\s{2,}", lines[0]) if p]
    loose = []
    for line in lines:
        m = re.match(r"^([^:=]{1,40}?)\s*[:=]\s*(.+)$", line)
        f = classify(m.group(1)) if m and not HOST.match(line) else None
        if f and f not in out:
            out[f] = clean(m.group(2))
        else:
            loose.append(clean(line))
    for v in list(loose):
        if "server" not in out and HOST.match(v):
            out["server"] = v
            loose.remove(v)
        elif "dir" not in out and re.match(r"^/?www/?$", v, re.I):
            out["dir"] = v
            loose.remove(v)
    for f in ("username", "password"):
        if f not in out and loose:
            out[f] = loose.pop(0)
    return out


cfg = {
    "server": os.environ.get("FTP_SERVER", ""),
    "username": os.environ.get("FTP_USERNAME", ""),
    "password": os.environ.get("FTP_PASSWORD", ""),
    "dir": os.environ.get("FTP_DIR", ""),
}
cfg = {k: clean(v) for k, v in cfg.items() if clean(v)}
for k, v in parse(os.environ.get("DETAL", "")).items():
    cfg.setdefault(k, v)

if "server" in cfg:
    m = HOST.match(cfg["server"])
    if m:
        cfg["server"] = m.group(1)
cfg["dir"] = cfg.get("dir", "www").strip("/").lstrip(".").strip("/") + "/"
if cfg["dir"] == "/":
    cfg["dir"] = "./"

print("Rozpoznane pola:", ", ".join(k for k in ("server", "username", "password", "dir") if k in cfg))
missing = [k for k in ("server", "username", "password") if k not in cfg]
if missing:
    print("::error::Brakuje danych FTP:", ", ".join(missing))
    sys.exit(1)
if not HOST.match(cfg["server"]):
    print("::error::Adres serwera FTP nie wygląda na nazwę hosta")
    sys.exit(1)

for v in cfg.values():
    print(f"::add-mask::{v}")
with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
    for k, v in cfg.items():
        fh.write(f"{k}={v}\n")
