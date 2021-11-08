import utils
import time


def bfs(begin_state: list, end_state: list):
    name = 'dfs'  # 算法名称
    open_table = []  # open表
    closed_table = []  # close表
    step = 0  # 操作步数
    path = []  # 路径
    longest_path = []  # 最长搜索链
    max_search_length = 0  # 最长搜索链长度
    max_search_end_map = None  # 最长搜索链最后节点
    flag = False  # 是否成功

    print("searching bfs...")

    start_time = time.time()

    begin_map = {"state": begin_state, "depth": 0,
                 "parent": None}  # 在bfs中，depth表示节点扩展深度，即路径长度
    open_table.append(begin_map)

    # 当还有没探索过的节点时
    while len(open_table):
        current_map = open_table[0].copy()  # 宽度优先：考虑队列中第一个节点
        current_state = current_map.get("state")
        current_depth = current_map.get("depth")
        closed_table.append(open_table.pop(0))
        step += 1
        if current_depth >= max_search_length:
            max_search_length = current_depth
            max_search_end_map = current_map.copy()
        if utils.is_same(current_map.get("state"), end_state):
            flag = True
            break

        # 考虑可能的四个方向
        for i in range(4):
            if utils.can_move[i](current_state):
                new_map = {"state": utils.move[i](current_state),
                           "depth": current_map.get("depth")+1,
                           "parent": current_state}
                if (utils.in_list(new_map, open_table) == -1) and \
                        (utils.in_list(new_map, closed_table) == -1):
                    open_table.append(new_map)

    end_time = time.time()
    total_time = (end_time - start_time) * 1000

    # 统计情况（包含路径、搜索时间、搜索节点数、最长搜索链）
    utils.find_path(path, current_map, closed_table)
    utils.find_path(longest_path, max_search_end_map, closed_table)
    stats = {
        "name": name,
        "flag": flag,
        "path": path,
        "runtime": '{:.4f}'.format(total_time),
        "step": step,
        "longest": longest_path}

    return stats


if __name__ == '__main__':
    begin_state, end_state = utils.init_state()
    # begin_state = [1, 2, 3, 4, 5, 0, 7, 8, 6]
    stats = bfs(begin_state, end_state)
    utils.print_stats(stats)
