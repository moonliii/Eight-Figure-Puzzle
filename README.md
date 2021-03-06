# DFS, BFS, A*三种搜索算法解8数码问题

### 问题描述

- 3×3九宫棋盘，放置数码为1 -8的8个棋盘，剩下一个空格，只能通过棋盘向空格的移动来改变棋盘的布局。

- 要求：根据给定初始布局（即初始状态）和目标布局（即目标状态），如何移动棋牌才能从初始布局到达目标布局，找到合法的走步序列。

- 实现：

  - DFS、BFS、A*算法（包含四种启发函数）
  - 可扩展到15数码问题

  - 显示搜索了多少节点
  - 显示搜索使用了多长时间
  - 显示八数码问题中最长的一个搜索链
  - 动态演示搜索过程

### 编程语言

- python（可视化部分使用 `PyQt5`）

### 整体分析

- 是否有解：初始序列和目标序列在**逆序数**的奇偶性上，是否同奇同偶

- 棋盘上数码排列情况，一共有9！种不同状态。每个状态和一个数码序列（从左到右从上到下降维）一一映射

- 制定操作算子集：

  - 直观方法——为每个棋牌制定一套可能的走步：左、上、右、下四种移动。这样就需32个操作算子。

  - 简易方法——仅为空格制定这4种走步，因为只有紧靠空格的棋牌才能移动。

    > 空格移动的唯一约束是不能移出棋盘。 

- 数据结构

  - 基础元素结构

    `map = {"state":[], "G":0 , "H":H(begin_state, end_state), "parent":[]}`

  - open表与closed表

    - open表：记录已经生成但未扩展的状态

    - closed表：记录已经扩展过的状态

    - 在不同的搜索策略中，open表的结构是不同的
      - 深度优先中：栈
      - 宽度优先中：队列
      - A*算法中：按照f值由小到大排列（类似优先队列）

### 算法分析

#### DFS

- 深度优先是按照一定的顺序前查找完一个分支，再查找另一个分支，以至找到目标为止。

- 防止搜索过程沿着无益的路径扩展下去，往往给出一个节点扩展的最大深度.

  > 在实验中定义max_depth = map_size * map_size

#### BFS

- 广度优先是从初始状态一层一层向下找，直到找到目标为止。

#### A*

- **启发式搜索**（*使用启发式信息指导的搜索过程称为启发式搜索*）就是在状态空间中的搜索对每一个搜索的位置进行评估，得到最好的位置，再从这个位置进行**扩展节点**直到目标。

- 启发中的估价是用**估价函数**表示的，如：f(n) = g(n) +h(n)其中f(n) 是节点n的估价函数，g(n)是在状态空间中从初始节点到n节点的实际代价（**扩展深度**），h(n)是从n到目标节点最佳路径的估计代价（**启发函数**）。

- 启发函数设计

  1. 启发函数h(n)定义为当前节点与目标节点差异的度量：即当前节点与目标节点格局相比，位置不符的数字个数。
  2. 启发函数h(n)定义为当前节点与目标节点距离的度量：当前节点与目标节点格局相比，位置不符的数字移动到目标节点中对应位置的最短距离之和。
  3. 启发函数h(n)定义为每一对逆序数字乘以一个倍数。
  4. 为克服了仅计算数字逆序数字数目策略的局限，启发函数h(n)定义为位置不符数字个数的总和与3倍数字逆序数目相加。

- 主过程伪代码

  ```
  begin: 
       检查目标状态到状态序列是否可达，可达继续操作
       open=[begin_map]  ,closed=[]  //将初始结点放到open表中
   
       while(open!=[] )  //当open表不为空时，执行循环
      {
        将open表的第一个结点n出栈，
        if n.state= 目标.state, then return (success)
        记录结点n的路径
        移动结点n的空格部分，生成结点n的子节点    // 可以移动到的子节点
        对n的子节点的状态序列state
        
        case: 出现在open表中过
               if 子结点的f值<open表中的结点f值，
               then 将原来open表中的node删除，记录新生成的子节点的路径和f值，放入open表中
        case: 在closed表中出现过
               if 子节点的f值<closed表中的结点f值
               then 将原来的closed表中的node删除，记录记录新生成的子节点的路径和f值，放入open表中
        case: 未在open表和closed表中出现过
              then 将新的结点放入open表中
   
      }
       return failure;
  end;
  ```

### 测试方式

- 运行EightFigurePuzzle文件夹里的`visualization.py`文件
