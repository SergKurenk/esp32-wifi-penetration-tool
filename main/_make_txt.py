import re
from pathlib import Path

FILES = [
    "main/attack.c",
    "main/attack.h",
    "main/attack_dos.c",
    "main/attack_dos.h",
    "main/attack_handshake.c",
    "main/attack_handshake.h",
    "main/attack_method.c",
    "main/Aattack_method.h",
    "main/attack_pmkid.c",
    "main/attack_pmkid.h",
	"main/CMakeLists.txt",
	"main/main.c",
    "components/webserver/utils/index.html",
	"components/webserver/webserver.c",
	"components/frame_analyzer/frame_analyzer.c",
	"components/frame_analyzer/frame_analyzer_parser.c",
	"components/hccapx_serializer/hccapx_serializer.c",
    "components/pcap_serializer/pcap_serializer.c",
    "components/wifi_controller/ap_scanner.c",
    "components/wifi_controller/ap_scanner.h",
    "components/wifi_controller/sniffer.c",
    "components/wifi_controller/sniffer.h",
    "components/wifi_controller/wifi_controller.c",
    "components/wsl_bypasser/wsl_bypasser.c"
]

OUTPUT = "ALL_SOURCES_CLEAN.txt"

# ===== Видалення коментарів =====

def remove_cpp_comments(code: str) -> str:
    # C/C++/JS style: //… і /* … */
    # але не чіпає строки в лапках
    pattern = r"""
        ("(?:\\.|[^"\\])*")            # рядки в "
      | ('(?:\\.|[^'\\])*')            # рядки в '
      | (/\*.*?\*/|//[^\n]*)           # коментарі
    """
    regex = re.compile(pattern, re.VERBOSE | re.DOTALL)

    def repl(m):
        # якщо це коментар — замінюємо на пусто
        if m.group(3):
            return ""
        return m.group(1) or m.group(2) or ""

    return regex.sub(repl, code)


def remove_html_comments(code: str) -> str:
    # прибираємо HTML-коментарі <!-- -->
    return re.sub(r"<!--(?!<!)(?:(?!-->).)*-->", "", code, flags=re.DOTALL)


def clean_whitespace(code: str) -> str:
    # прибрати зайві пробіли та пусті строки
    lines = [ln.strip() for ln in code.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def process_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    ext = path.suffix.lower()

    # HTML
    if ext in {".html", ".htm"}:
        # 1) прибрати HTML-коментарі
        text = remove_html_comments(text)
        # 2) з HTML видалити JS і CSS коментарі теж
        text = remove_cpp_comments(text)

    # C/C++/INO/JS
    elif ext in {".c", ".cpp", ".h", ".ino", ".js"}:
        text = remove_cpp_comments(text)

    # CSS (якщо окремий файл)
    elif ext == ".css":
        # remove /* */ CSS comments
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

    return clean_whitespace(text)


with open(OUTPUT, "w", encoding="utf-8") as out:
    out.write("=== MERGED & CLEANED SOURCES ===\n")

    for f in FILES:
        path = Path(f)
        # path = Path("src/"+f)
        out.write(f"\n=== FILE: {f} ===\n")
        if path.exists():
            out.write(process_file(path))
        else:
            out.write("!!! NOT FOUND !!!\n")

# print(f"Done! -> {OUTPUT}. Filesize: {out.__sizeof__}")
size_kb = Path(OUTPUT).stat().st_size / 1024
print(f"Done! -> {OUTPUT}. Filesize: {size_kb:.2f} KB")