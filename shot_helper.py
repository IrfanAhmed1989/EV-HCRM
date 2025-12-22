import os, sys
step = sys.argv[1]
png = sys.argv[2]
print(f"\n📸 {step}: Bring the window/dialog to front, then press Enter to capture -> {png}")
input()
os.system(f'screencapture -x "{png}"')
print(f"✅ Saved {png}")
