#!/usr/bin/env python3
import sys
import shutil
import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
AGENTS_DIR = BASE_DIR / 'agents'
TEMPLATES_DIR = BASE_DIR / 'agents_templates'

def switch_theme(theme_name):
    if theme_name not in ('shengbu', 'hougong'):
        print(f"Unknown theme: {theme_name}")
        sys.exit(1)
        
    source_dir = TEMPLATES_DIR / theme_name
    if not source_dir.exists():
        print(f"Template directory {source_dir} not found!")
        sys.exit(1)
        
    for agent_dir in source_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        agent_id = agent_dir.name
        target_dir = AGENTS_DIR / agent_id
        
        # We only overwrite SOUL.md to avoid messing with sessions or other data
        source_soul = agent_dir / 'SOUL.md'
        target_soul = target_dir / 'SOUL.md'
        
        if source_soul.exists() and target_dir.exists():
            shutil.copy2(source_soul, target_soul)
            print(f"Swapped {agent_id} SOUL.md to {theme_name} theme.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: switch_theme.py <shengbu|hougong>")
        sys.exit(1)
    switch_theme(sys.argv[1])
