import time
import utils


def H1(current_state: list, end_state: list):
    """启发函数1：找当前状态与目标状态的位置不同的非0数字个数"""
    cost = 0
    for idx in range(utils.map_size * utils.map_size):
        if current_state[idx] != end_state[idx]:
            cost += 1
    return cost


def H2(current_state: list, end_state: list):
    """启发函数2：找当前状态要移动到目标的最短路径，返回所有状态的最短路径之和"""
    cost = 0
    size = utils.map_size
    for idx, num in enumerate(current_state):
        end_idx = end_state.index(num)
        end_x, end_y = int(end_idx/size), end_idx % size
        current_x, current_y = int(idx/size), idx % size
        cost += abs(current_x - end_x) + abs(current_y-end_y)
    return cost


def H3(current_state: list, end_state: list):
    """启发函数3：返回逆序数目*3"""
    return 3 * utils.get_inversion_num(current_state)


def H4(current_state: list, end_state: list):
    """启发函数4：综合H1与H3"""
    return H1(current_state, end_state) + H3(current_state, end_state)


H_list = [H1, H2, H3, H4]
H = H_list[utils.h_type-1]


def F(current_map):
    return current_map.get("G") + current_map.get("H")  # F = G + H


def a_star(begin_state: list, end_state: list):
    name = 'a-star'  # 算法名称
    open_table = []  # open表
    closed_table = []  # close表
    step = 0  # 操作步数（搜索的节点数）
    path = []  # 路径
    longest_path = []  # 最长搜索链
    max_search_length = 0  # 最长搜索链长度
    max_search_end_map = None  # 最长搜索链最后节点
    flag = False  # 是否成功

    print("searching a-star...")

    start_time = time.time()

    # 在a-star中，G表示从初始节点到当前节点的实际代价，H表示到目标节点最佳路径的估计代价
    begin_map = {"state": begin_state, "G": 0, "H": H(begin_state, end_state),
                 "parent": None}
    open_table.append(begin_map)

    while len(open_table):
        current_map = open_table[0].copy()  # a-star, 考虑估价函数F=G+H最小的节点
        current_state = current_map.get("state")
        current_depth = current_map.get("G")
        closed_table.append(open_table.pop(0))
        step += 1
        if current_depth >= max_search_length:
            max_search_length = current_depth
            max_search_end_map = current_map.copy()
        if utils.is_same(current_state, end_state):
            flag = True
            break

        # 考虑可能的四个方向
        for i in range(4):
            if utils.can_move[i](current_state):
                new_state = utils.move[i](current_state)
                new_map = {"state": new_state,
                           "G": current_map.get("G")+1,
                           "H": H(new_state, end_state),
                           "parent": current_state}
                # 在open表中出现过，更新F值（但相同的state的H值相同，故比较G值）
                open_idx = utils.in_list(new_map, open_table)
                if open_idx != -1:
                    if new_map.get("G") < open_table[open_idx].get("G"):
                        open_table[open_idx] = new_map.copy()
                        break
                # 在closed表中出现，将closed表中原节点删除，将新节点放入open表
                closed_idx = utils.in_list(new_map, closed_table)
                if closed_idx != -1:
                    if new_map.get("G") < closed_table[closed_idx].get("G"):
                        closed_table.pop(closed_idx)
                        open_table.append(new_map)
                # 在open表和closed表中没出现过，加入open表
                if closed_idx == -1 and open_idx == -1:
                    open_table.append(new_map)

        open_table.sort(key=F)  # 根据估价函数F升序排序

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
    stats = a_star(begin_state, end_state)
    utils.print_stats(stats)
