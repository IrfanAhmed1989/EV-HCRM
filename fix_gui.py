from pathlib import Path

gui_p = Path("GUI.py")
gui = gui_p.read_text().splitlines()

fixed_lines = []
for line in gui:
    # Remove any stray spaces before top-level code
    if line.startswith("    app = EVHCRMApp(root)"):
        fixed_lines.append("app = EVHCRMApp(root)")
    else:
        fixed_lines.append(line)

# Ensure login block is properly aligned
if "temp_root = tk.Tk()" in "\n".join(fixed_lines):
    # Normalize indentation for injected block
    fixed_lines = [l.lstrip() for l in fixed_lines]

gui_p.write_text("\n".join(fixed_lines))
print("✅ Indentation fixed. GUI.py normalized.")
