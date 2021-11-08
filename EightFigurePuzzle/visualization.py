from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication, QGridLayout,  QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt, QTimer
import utils
import sys
from dfs import dfs
from bfs import bfs
from a_star import a_star


class MainPage(QWidget):
    """ 主体窗口"""

    def __init__(self, begin_state):
        super().__init__()
        self.init_params()
        self.init_main_page(begin_state)

    def init_params(self):
        self.timer = QTimer(self)  # board更新的计时器
        self.timer.timeout.connect(show_one_path)

    def init_main_page(self, begin_state):
        hbox = QHBoxLayout()
        self.setLayout(hbox)  # 水平箱布局
        self.setWindowTitle('Eight-Digit_Puzzle by Liyue')  # 设置标题
        self.setFixedSize(utils.window_width, utils.window_height)  # 设置宽和高
        self.setStyleSheet('background-color: white;')  # 设置背景颜色

        self.board = MapBoard(begin_state)
        self.info_sector = InfoSector()
        hbox.addWidget(self.board)
        hbox.addWidget(self.info_sector)
        self.show()


class MapBoard(QWidget):
    """八/十五数码展示板"""

    def __init__(self, begin_state):
        super().__init__()
        self.init_params()
        self.init_board()
        self.update_board(begin_state)

    def init_board(self):
        self.grid = QGridLayout()  # 网格布局
        self.setFixedSize(utils.board_width, utils.board_height)

    def init_params(self):
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0

    def update_board(self, state):
        self.blocks.clear()
        # 删除原来的widget
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().deleteLater()

        # 将数字添加到二维数组
        for row in range(utils.map_size):
            self.blocks.append([])
            for column in range(utils.map_size):
                num = state[row * utils.map_size + column]
                if num == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(num)

        for row in range(utils.map_size):
            for column in range(utils.map_size):
                self.grid.addWidget(
                    Block(self.blocks[row][column]), row, column)
        self.setLayout(self.grid)


class Block(QLabel):
    """数字方块"""

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(utils.block_size, utils.block_size)

        # 设置字体
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        self.setFont(font)

        # 设置字体颜色
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # 设置文字位置
        self.setAlignment(Qt.AlignCenter)

        # 设置背景颜色、圆角、文本内容
        if self.number == 0:
            self.setStyleSheet("background-color:white;")
        else:
            self.setStyleSheet("background-color:black;")
            self.setText(str(self.number))


class InfoSector(QWidget):
    """展示运行信息的区域"""

    def __init__(self):
        super().__init__()

        self.init_params()
        self.init_info_sector()

    def init_params(self):
        self.algorithm = 'DFS'
        self.runtime = 0
        self.count = 0
        self.step = 0
        self.longest = 0

    def init_info_sector(self):
        vbox = QVBoxLayout()  # 垂直箱布局
        self.setLayout(vbox)
        self.setFixedSize(utils.info_height, utils.info_height)

        # 算法选择
        al_label = QLabel()
        al_label.setText('请选择搜索算法')
        al_label.setFixedSize(utils.info_width, 20)
        al_combo = QComboBox(self)
        al_combo.addItem('DFS')
        al_combo.addItem('BFS')
        al_combo.addItem('A*')
        al_combo.activated[str].connect(self.on_algorithm_chosen)
        vbox.addWidget(al_label)
        vbox.addWidget(al_combo)

        # 8数码还是15数码
        type_label = QLabel()
        type_label.setText('请选择8或是15数码')
        type_label.setFixedSize(utils.info_width, 20)
        type_combo = QComboBox(self)
        type_combo.addItem('8')
        type_combo.addItem('15')
        type_combo.activated[str].connect(self.on_type_chosen)
        vbox.addWidget(type_label)
        vbox.addWidget(type_combo)

        # 开始运行button
        start_button = QPushButton('开始运行')
        start_button.clicked.connect(start_search)
        vbox.addWidget(start_button)

        # 重置
        reset_button = QPushButton('重置')
        reset_button.clicked.connect(reset_search)
        vbox.addWidget(reset_button)

        # 开始、结束状态
        self.begin_label = QLabel()
        self.begin_label.setText('开始状态：'+utils.list_to_str(begin_state))
        self.end_label = QLabel()
        self.end_label.setText('结束状态：'+utils.list_to_str(end_state))
        vbox.addWidget(self.begin_label)
        vbox.addWidget(self.end_label)

        # 运行信息
        self.runtime_label = QLabel()
        self.runtime_label.setText('搜索时间为：'+f'{self.runtime}' + ' ms')
        self.step_label = QLabel()
        self.step_label.setText('一共搜索的节点数为：' + f'{self.step}')
        self.count_label = QLabel()
        self.count_label.setText('路径长度为：'+f'{self.count}')
        self.longest_label = QLabel()
        self.longest_label.setText('最长搜索链长度为：'+f'{self.longest}')
        vbox.addWidget(self.runtime_label)
        vbox.addWidget(self.step_label)
        vbox.addWidget(self.count_label)
        vbox.addWidget(self.longest_label)

    def on_algorithm_chosen(self, text):
        self.algorithm = text
        reset_UI()
        print('choose '+text)

    def on_type_chosen(self, text):
        """修改全局map_size 重新绘制board"""
        utils.map_size = 3 if text == '8' else 4
        reset_search()
        print('choose '+text+'-digit')

    def update_info(self):
        self.runtime_label.setText('搜索时间为：'+f'{self.runtime}' + ' ms')
        self.step_label.setText('一共搜索的节点数为：' + f'{self.step}')
        self.count_label.setText('路径长度为：'+f'{self.count}')
        self.longest_label.setText('最长搜索链长度为：'+f'{self.longest}')
        self.begin_label.setText('开始状态：'+utils.list_to_str(begin_state))
        self.end_label.setText('结束状态：'+utils.list_to_str(end_state))


def reset_search():
    global begin_state, end_state
    begin_state, end_state = utils.init_state()
    reset_UI()


def reset_UI():
    main_page.board.update_board(begin_state)
    main_page.info_sector.runtime = main_page.info_sector.step =\
        main_page.info_sector.count = main_page.info_sector.longest = 0
    main_page.info_sector.update_info()


def start_search():
    global result_stats
    # 开始逻辑
    algorithm = main_page.info_sector.algorithm
    if algorithm == 'DFS':
        result_stats = dfs(begin_state, end_state)
    elif algorithm == 'BFS':
        result_stats = bfs(begin_state, end_state)
    elif algorithm == 'A*':
        result_stats = a_star(begin_state, end_state)
    set_info(result_stats)
    if result_stats['flag']:
        main_page.timer.start(500)  # 每次更新地图间隔500ms
    else:
        QMessageBox.information(
            main_page, '', 'Sorry, No solution within finite depth!', QMessageBox.Yes)
    utils.print_stats(result_stats)


def set_info(stats: dict):
    """显示搜索结束的统计情况"""
    if stats is not None:
        main_page.info_sector.runtime = stats['runtime']
        main_page.info_sector.step = stats['step']
        main_page.info_sector.count = len(stats['path'])
        main_page.info_sector.longest = len(stats['longest'])
    main_page.info_sector.update_info()


def show_one_path():
    """显示搜索过程"""
    path = result_stats['path']
    if len(path) != 0:
        current_state = path.pop()
        # print(len(path))
        main_page.board.update_board(current_state)
    else:
        main_page.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    begin_state, end_state = utils.init_state()
    result_stats = None
    main_page = MainPage(begin_state)
    sys.exit(app.exec_())
