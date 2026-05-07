# 三省六部制协作架构 (Shengbu Topology)

## 状态定义与流转 (States and Flow)

| 状态栏 (State) | 角色名称 (Role Label) | 绑定代理 (Agent ID) | 下游状态 (Next State) | 说明 (Description)                           |
| -------------- | --------------------- | ------------------- | --------------------- | -------------------------------------------- |
| Inbox          | 皇上                  | user                | Pending               | 皇上发起旨意                                 |
| Pending        | 太子                  | taizi               | Zhongshu              | 太子负责分析旨意、自动回退或流转中书省       |
| Zhongshu       | 中书省                | zhongshu            | Menxia                | 起草执行方案                                 |
| Menxia         | 门下省                | menxia              | Assigned              | 审核方案，可打回 Zhongshu                    |
| Assigned       | 尚书省                | shangshu            | Doing                 | 派发任务给六部执行                           |
| Doing          | 执行中                | routing             | Review                | 六部并发执行                                 |
| Review         | 尚书省                | shangshu            | Done                  | 尚书省汇总六部结果，或提交门下省(Escalation) |
| Done           | 完结                  | -                   | -                     | 流程结束                                     |
| Blocked        | 阻塞                  | -                   | -                     | 任务被卡住需人工干预                         |

## 执行部门池 (Execution Pool)

当状态为 `Doing` 时，可以指派以下部门的代理：
- `libu` (礼部)
- `hubu` (户部)
- `bingbu` (兵部)
- `xingbu` (刑部)
- `gongbu` (工部)
- `libu_hr` (吏部)
- `zaochao` (钦天监)
