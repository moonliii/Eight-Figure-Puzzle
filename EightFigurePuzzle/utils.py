import random

map_size = 3  # 8数码；3*3，15数码：4*4
max_depth = 15  # dfs 最大深度 max_depth + 2
h_type = 2  # 默认选择H2启发函数

# GUI设置
window_width = 1200
window_height = 800
board_width = 800
board_height = 800
info_width = 400
info_height = 400
block_size = 120


def list_to_str(lst: list):
    str_list = [str(i) for i in lst]
    return ','.join(str_list)


def get_inversion_num(seq: list):
    """得到排列的逆序数"""
    cnt = 0
    for i in range(len(seq)):
        for j in range(i):
            if seq[j] > seq[i]:
                cnt += 1
    return cnt


def in_list(mp, map_list):
    """是否在表中出现过，若出现过，返回在列表中的下标，否则返回-1"""
    for idx, temp_map in enumerate(map_list):
        if is_same(mp.get("state"), temp_map.get("state")):
            return idx
    else:
        return -1


def init_state():
    """初始化地图的函数，通过从结束位置随机走来达到一定有解的目的"""
    end_state = []
    for i in range(1, map_size * map_size + 1):
        end_state.append(i)
    end_state[-1] = 0
    steps = random.randint(map_size * map_size * 2,
                           map_size * map_size * 2 + 5)
    i = 0
    begin_state = end_state.copy()
    while i < steps:
        mov = random.randint(0, 3)
        if can_move[mov](begin_state):
            begin_state = move[mov](begin_state)
            i += 1
    return begin_state, end_state


def is_same(state1, state2):
    i = 0
    while i < map_size * map_size:
        if state1[i] != state2[i]:
            return False
        i += 1
    return True


def get_zero_pos(state):
    i = 0
    while i < map_size * map_size:
        if state[i] == 0:
            return i
        i += 1
    return -1


def can_up(state):
    return get_zero_pos(state) - map_size > 0


def can_down(state):
    return get_zero_pos(state) + map_size < map_size * map_size


def can_left(state):
    return get_zero_pos(state) % map_size > 0


def can_right(state):
    return get_zero_pos(state) % map_size < map_size - 1


def move_up(state: list):
    state_cp = state.copy()
    zero_pos = get_zero_pos(state_cp)
    state_cp[zero_pos] = state_cp[zero_pos - map_size]
    state_cp[zero_pos - map_size] = 0
    return state_cp


def move_down(state: list):
    state_cp = state.copy()
    zero_pos = get_zero_pos(state_cp)
    state_cp[zero_pos] = state_cp[zero_pos + map_size]
    state_cp[zero_pos + map_size] = 0
    return state_cp


def move_left(state: list):
    state_cp = state.copy()
    zero_pos = get_zero_pos(state_cp)
    state_cp[zero_pos] = state_cp[zero_pos - 1]
    state_cp[zero_pos - 1] = 0
    return state_cp


def move_right(state: list):
    state_cp = state.copy()
    zero_pos = get_zero_pos(state_cp)
    state_cp[zero_pos] = state_cp[zero_pos + 1]
    state_cp[zero_pos + 1] = 0
    return state_cp


move = [move_up, move_down, move_left, move_right]
can_move = [can_up, can_down, can_left, can_right]


def find_path(path, current_map, closed_table):
    path.append(current_map.get("state"))
    parent_state = current_map.get("parent")
    while parent_state is not None:
        for closed_map in closed_table:
            if is_same(parent_state, closed_map.get("state")):
                path.append(parent_state)
                parent_state = closed_map.get("parent")
                break


def print_path(path: list):
    path_copy = path.copy()
    while len(path_copy):
        state = path_copy.pop()
        idx = 1
        for num in state:
            print("{0:4}".format(num), end='')
            if idx % map_size == 0:
                print('\n', end='')
            idx += 1
        print()


def print_stats(stats):
    print("The stats of {} algorithm in solving eight-digits-puzzle:".format(stats.get("name")))
    if not stats.get("flag"):
        print("No solution!")
    else:
        print("Path:")
        print_path(stats.get("path"))
    print("Total runtime: {} ms.".format(stats.get("runtime")))
    print("The number of nodes that have been searched: {}".format(stats.get("step")))
    print("The longest searching path:")
    print_path(stats.get("longest"))


if __name__ == '__main__':
    pass
