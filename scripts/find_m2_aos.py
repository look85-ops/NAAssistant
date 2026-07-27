#!/usr/bin/env python3
import os
import pandas as pd
import json
from pathlib import Path

# Debug: List all directories in Desktop
desktop = Path('C:\\Users\\marcenuk\\Desktop')

print("All directories in Desktop:")
for item in desktop.iterdir():
    if item.is_dir():
        print(f"  {item.name}")

print("\nAll files in Desktop:")
for item in desktop.iterdir():
    if item.is_file() and item.suffix in ['.xlsx', '.csv', '.xls']:
        print(f"  {item.name}")

# Try to find M2 directory
m2_path = None
for item in desktop.iterdir():
    if item.is_dir() and 'M2' in item.name:
        m2_path = item
        print(f"\nFound M2 directory: {item.name}")
        break

if m2_path:
    # List all files in M2 directory
    print(f"\nFiles in {m2_path}:")
    for item in m2_path.iterdir():
        if item.is_file():
            print(f"  {item.name}")
            
    # Try to read the AOS file
    aos_file = m2_path / 'AOS_A�ademi�Puti (M2_��бр�тка�e).xlsx'
    if aos_file.exists():
        print(f"\nFound AOS file: {aos_file}")
        try:
            # Read the Excel file
            df = pd.read_excel(aos_file, sheet_name=0)
            print(f"Data shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("\nFirst few rows:")
            print(df.head())
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        print(f"AOS file not found: {aos_file}")
        
        # List all .xlsx files
        xlsx_files = list(m2_path.glob('*.xlsx'))
        print(f"\nAvailable .xlsx files:")
        for file in xlsx_files:
            print(f"  {file.name}")
else:
    print("\nM2 directory not found")
