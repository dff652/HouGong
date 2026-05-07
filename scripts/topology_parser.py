import pathlib
import sys
import os

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
TOPOLOGIES_DIR = BASE_DIR / "topologies"

def parse_topology(mode: str) -> dict:
    md_path = TOPOLOGIES_DIR / f"{mode}.md"
    if not md_path.exists():
        if mode == 'hougong' and (TOPOLOGIES_DIR / 'shengbu.md').exists():
            return parse_topology('shengbu') # Fallback if error
        return {}
    
    lines = md_path.read_text('utf-8').splitlines()
    
    topology = {
        "mode": mode,
        "name": "",
        "columns": [],
        "states": {},
        "pool": {},
        "agent_to_state": {},
        "agent_to_label": {}
    }
    
    parsing_states = False
    parsing_pool = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("# "):
            topology["name"] = line[2:].strip()
            continue
            
        if line.startswith("## 状态定义"):
            parsing_states = True
            parsing_pool = False
            continue
            
        if line.startswith("## 执行部门池"):
            parsing_pool = True
            parsing_states = False
            continue
            
        if parsing_states and line.startswith("|") and not line.startswith("|---"):
            # Parse state table row
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 4 and parts[0] != "状态栏 (State)" and not set(parts[0]).issubset({'-', ' '}):
                state_id = parts[0]
                label = parts[1]
                agent_id = parts[2]
                next_state = parts[3]
                
                topology["columns"].append(state_id)
                topology["states"][state_id] = {
                    "label": label,
                    "agent_id": None if agent_id in ('-', 'routing', 'user') else agent_id,
                    "next": None if next_state == '-' else next_state,
                    "is_routing": agent_id == 'routing'
                }
                
                if agent_id not in ('-', 'routing', 'user'):
                    topology["agent_to_state"][agent_id] = state_id
                    topology["agent_to_label"][agent_id] = label
                    
        if parsing_pool and line.startswith("- `"):
            # Parse pool row e.g. - `libu` (礼部)
            import re
            m = re.match(r'- `([^`]+)` \(([^)]+)\)', line)
            if m:
                aid = m.group(1)
                lbl = m.group(2)
                topology["pool"][aid] = lbl
                topology["agent_to_label"][aid] = lbl
            else:
                m2 = re.match(r'- `([^`]+)`', line)
                if m2:
                    aid = m2.group(1)
                    topology["pool"][aid] = aid
                    topology["agent_to_label"][aid] = aid
                
    return topology

def get_current_topology():
    """Reads active mode from data/active_mode.txt for global consistency"""
    mode = 'shengbu'
    mode_file = BASE_DIR / 'data' / 'active_mode.txt'
    if mode_file.exists():
        mode = mode_file.read_text('utf-8').strip() or 'shengbu'
    return parse_topology(mode)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'shengbu'
    import json
    print(json.dumps(parse_topology(mode), indent=2, ensure_ascii=False))
