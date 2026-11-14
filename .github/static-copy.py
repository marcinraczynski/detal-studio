"""Wpisuje polskie teksty z obiektu `dict` na stałe do index.html.

Roboty, które nie uruchamiają JavaScriptu (większość robotów AI), widzą dzięki
temu całą treść. Skrypt na stronie i tak podmienia teksty przy zmianie języka.
Uruchamiany przy wdrożeniu i ręcznie po zmianie tekstów: python3 .github/static-copy.py
"""
import html, re, sys

PATH = "index.html"
src = open(PATH, encoding="utf-8").read()

block = re.search(r"\bpl:\s*\{(.*?)\n\s*\},\s*\n\s*en:\s*\{", src, re.S)
if not block:
    sys.exit("Nie znaleziono polskich tekstów w index.html")
pl = {k: v.replace('\\"', '"') for k, v in re.findall(r'(\w+):"((?:[^"\\]|\\.)*)"', block.group(1))}


def nb(s):
    # to samo co funkcja nb() na stronie: jedno- i dwuliterowe słowa trzymają się następnego wyrazu
    for _ in range(2):
        s = re.sub(r"(^|[\s>(;])([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9]{1,2})\s+(?=[^\s<])", r"\1\2&nbsp;", s)
    return s


# komunikaty, które pojawiają się dopiero po akcji użytkownika, zostają puste (wypełnia je skrypt)
SKIP = {"doneH", "doneP", "ckText", "ckNo", "ckYes"}
missing = set()


def fill(m):
    key = m.group(3)
    if key in SKIP:
        return m.group(1) + m.group(5)
    if key not in pl:
        missing.add(key)
        return m.group(0)
    return m.group(1) + nb(pl[key]) + m.group(5)


out = re.sub(r'(<(\w+)\b[^>]*\bdata-i18n="(\w+)"[^>]*>)(.*?)(</\2>)', fill, src, flags=re.S)


def placeholder(m):
    tag, key = m.group(0), m.group(1)
    if key not in pl:
        missing.add(key)
        return tag
    tag = re.sub(r'\splaceholder="[^"]*"', "", tag)
    return tag[:-1] + ' placeholder="' + html.escape(pl[key], quote=True) + '">'


out = re.sub(r'<(?:input|textarea)\b[^>]*\bdata-i18n-ph="(\w+)"[^>]*>', placeholder, out)

if missing:
    sys.exit("Brak tekstów dla kluczy: " + ", ".join(sorted(missing)))
if out != src:
    open(PATH, "w", encoding="utf-8").write(out)
print("Teksty wpisane:", len(re.findall(r'data-i18n="', out)), "elementów")
