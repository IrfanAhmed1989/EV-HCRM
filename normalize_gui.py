from pathlib import Path

gui_p = Path("GUI.py")
lines = gui_p.read_text().splitlines()

normalized = []
for line in lines:
    # If line starts with spaces but is not inside a function/class, strip it
    if line.startswith("    ") and not line.lstrip().startswith(("def ", "class ", "#")):
        normalized.append(line.lstrip())
    else:
        normalized.append(line)

gui_p.write_text("\n".join(normalized))
print("✅ GUI.py indentation normalized.")
