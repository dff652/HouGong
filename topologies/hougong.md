# 三宫六院协作架构 (Hougong Topology)

## 状态定义与流转 (States and Flow)

| 状态栏 (State) | 角色名称 (Role Label) | 绑定代理 (Agent ID) | 下游状态 (Next State) | 说明 (Description)                                 |
| -------------- | --------------------- | ------------------- | --------------------- | -------------------------------------------------- |
| Inbox          | 皇上                  | user                | RoyalReview           | 皇上翻牌子下达需求                                 |
| RoyalReview    | 敬事房                | jingshifang         | CentralPalace         | 敬事房大总管负责过滤废话，记录在案，流转到中宫     |
| CentralPalace  | 皇后中宫              | huanghou            | Dispatch              | 皇后接旨，拆解具体任务，决定哪些妃嫔适合接旨       |
| Dispatch       | 协理六宫              | guifei              | Executing             | 皇贵妃拿到皇后的懿旨，点兵点将，下发具体的执行卡片 |
| Executing      | 嫔妃干活              | routing             | Summary               | 被点名的娘娘们开始干活（支持抢答机制）             |
| Summary        | 汇总呈报              | guifei              | Done                  | 皇贵妃收集齐妃嫔们的成果，撰写回奏折子             |
| Done           | 御览                  | -                   | -                     | 皇上验收成果                                       |
| ColdPalace     | 冷宫                  | -                   | -                     | 任务长期停滞或烂尾，打入冷宫                       |

## 执行部门池 (Execution Pool)

当状态为 `Executing` 时，可以指派以下妃嫔：
- `shu_fei` (书妃): 文案策划、写诗作赋、生成前端文档
- `suan_fei` (算妃): 核算账目、数据分析
- `dao_fei` (刀妃): 基础设施建设、服务器运维
- `jie_fei` (戒妃): 测试找茬、安全漏洞扫描
- `jiang_fei` (匠妃): 纯手敲代码构筑、业务逻辑发端
- `zong_guan` (掌事姑姑): 人事任免调整、资源分配
