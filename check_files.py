import os
import sys

folder = r"C:\Users\marcenuk\Desktop\Новый проект"
print(f"Checking folder: {folder}")
print(f"Exists: {os.path.exists(folder)}")

if os.path.exists(folder):
    files = os.listdir(folder)
    print(f"Files found: {len(files)}")
    for f in files:
        print(f"  - {f}")
