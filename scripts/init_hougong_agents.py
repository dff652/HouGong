import sys
import shutil
import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
AGENTS_DIR = BASE_DIR / 'agents'
TEMPLATES_DIR = BASE_DIR / 'agents_templates' / 'hougong'

# Topology and ID translation map
TRANSLATIONS = {
    # Workflow states
    "Zhongshu": "CentralPalace",
    "Menxia": "Dispatch",
    "Assigned": "Dispatch",
    "Taizi": "RoyalReview",
    "Doing": "Executing",
    "Review": "Summary",
    
    # Agent IDs
    "zhongshu": "huanghou",
    "menxia": "guifei",
    "shangshu": "guifei",
    "taizi": "jingshifang",
    "libu": "shu_fei",
    "hubu": "suan_fei",
    "bingbu": "dao_fei",
    "xingbu": "jie_fei",
    "gongbu": "jiang_fei",
    "libu_hr": "zong_guan",
    "zaochao": "qing_an",

    # Display names
    "中书省": "皇后",
    "门下省": "贵妃", 
    "尚书省": "贵妃",
    "太子": "敬事房",
    "礼部": "书妃",
    "户部": "算妃",
    "兵部": "刀妃",
    "刑部": "戒妃",
    "工部": "匠妃",
    "吏部": "掌事姑姑",
    "六部": "各宫娘娘",
}

# Source dir to new dir mapping
MAPPING = {
    "taizi": "jingshifang",
    "zhongshu": "huanghou",
    "shangshu": "guifei",
    "libu": "shu_fei",
    "hubu": "suan_fei",
    "bingbu": "dao_fei",
    "xingbu": "jie_fei",
    "gongbu": "jiang_fei",
    "libu_hr": "zong_guan",
}

for old_id, new_id in MAPPING.items():
    source_template = TEMPLATES_DIR / old_id / 'SOUL.md'
    if not source_template.exists():
        continue
        
    target_dir = AGENTS_DIR / new_id
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Read template prompt
    content = source_template.read_text(encoding='utf-8')
    
    # Apply translations
    for k, v in TRANSLATIONS.items():
        # Avoid replacing inside words if necessary, but simple replace works for these distinct tokens
        content = content.replace(k, v)
        
    # Inject topology awareness
    topology_notice = f"\n> **架构说明**：请务必阅读工作目录下的 `topologies/hougong.md` 文件了解你的上下游协作对象与流转状态！\n"
    if "架构说明" not in content:
        content = content.replace("> **身份设定", topology_notice + "\n> **身份设定")
        
    # Write new SOUL.md
    (target_dir / 'SOUL.md').write_text(content, encoding='utf-8')
    
    # Copy agent config if it exists in old agent
    old_agent_dir = AGENTS_DIR / old_id
    if (old_agent_dir / 'config.json').exists():
        shutil.copy2(old_agent_dir / 'config.json', target_dir / 'config.json')

print("Hougong isolated agents initialized successfully.")
