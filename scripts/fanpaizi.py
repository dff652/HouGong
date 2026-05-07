#!/usr/bin/env python3
import sys
import json
import random
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
STATS_FILE = DATA_DIR / 'officials_stats.json'

def get_weighted_random_official():
    try:
        with open(STATS_FILE, 'r') as f:
            data = json.load(f)
    except Exception:
        data = {}

    officials = data.get('officials', []) if isinstance(data, dict) else data
    if not officials:
        return random.choice(['hubu', 'libu', 'bingbu', 'xingbu', 'gongbu'])

    candidates = []
    for o in officials:
        aid = o.get('id', '')
        if aid not in ('hubu', 'libu', 'bingbu', 'xingbu', 'gongbu', 'libu_hr'):
            continue
        
        weight = float(o.get('merit_score', 10))
        if weight <= 0:
            continue # Cold Palace
            
        candidates.append((aid, o.get('label', aid), weight))

    if not candidates:
         return random.choice(['hubu', 'libu', 'bingbu', 'xingbu', 'gongbu'])

    agents, labels, weights = zip(*candidates)
    picked = random.choices(agents, weights=weights, k=1)[0]
    return picked

if __name__ == '__main__':
    picked = get_weighted_random_official()
    print(f"✅ 翻牌子结果 (Randomized Dispatch): {picked}")
