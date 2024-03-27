from kivy.config import Config
Config.set("graphics","resizable",0)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout
from kivy.clock import Clock
import random
Window.size=(350,600)

P=0
EMPTY_SQUARE = 0

class Pole(MDGridLayout):
    def replace(self,x,y):
        global P
        text_x = self.children[x]
        text_y = self.children[y]
        self.children[x] = text_y
        self.children[y] = text_x
        P = y
        app.fix[x], app.fix[y] = app.fix[y], app.fix[x]

        if app.fix == app.correct_board:
            app.switch_screen('result')
            old = app.config.get("Top","rec")
            app.screen.ids.r_time.text = app.time
            if app.time < old:
                app.config.set("Top","rec",app.time)
                app.config.write()
                app.screen.ids.m_rec.text=app.time

    def sdvig(self, x):
        global P
        if (x == 'up'):
            if P - 4 >= 0:
                self.replace(P, P - 4)

        if (x == 'down'):
            if P + 4 <= 15:
                self.replace(P, P + 4)
        if (x == 'right'):
            if (P + 1) % 4 != 0:
                self.replace(P, P + 1)
        if (x == 'left'):
            if P % 4 != 0:
                self.replace(P, P - 1)

    def on_touch_down(self, touch):
        touch.ud["x"] = touch.x
        touch.ud["y"] = touch.y

    def on_touch_up(self, touch):
        x = touch.ud["x"] - touch.x
        y = touch.ud["y"] - touch.y
        if (abs(x) - abs(y) > 0):
            if (x > 0):
                self.sdvig("left")
            else:
                self.sdvig("right")
        else:
            if y > 0:
                self.sdvig("down")
            else:
                self.sdvig("up")

class GameApp(MDApp):

    def get_inv_count(self):
        invers = 0
        invers_board = self.ORDER[:]
        invers_board.remove(EMPTY_SQUARE)
        for i in range(len(invers_board)):
            first = invers_board[i]
            for j in range(i + 1, len(invers_board)):
                second = invers_board[j]
                if first > second:
                    invers += 1
        return invers

    def is_solvable(self):
        num_inversions = self.get_inv_count()
        if num_inversions % 2 != 0:
            return num_inversions % 2 == 0
        else:
            empty_square_row = 4 - (self.ORDER.index(EMPTY_SQUARE) // 4)
            if empty_square_row % 2 == 0:
                return num_inversions % 2 != 0
            else:
                return num_inversions % 2 == 0

    def build(self):
        self.screen = Builder.load_file('ui.kv')
        self.time = '00:00'
        self.tick = 0
        self.i_timer = Clock.schedule_interval(callback=self.timer, timeout=1)
        self.ORDER = list(range(1, 17))
        self.correct_board = self.ORDER[:]
        return self.screen

    def build_config(self, config):
        config.setdefaults(
            'Top', {
                'rec':'00:00'
            }
        )
    def GigaRandom(self,a):
        a.remove(EMPTY_SQUARE)
        for i in range(14):
            self.screen.ids[f'm{i}'].text = str(a[i])

        self.screen.ids.m15.text = ""
        self.fix.append(15)
        self.fix.append(0)
        self.fix.reverse()


    def new_game(self):
        self.tick = 0
        app.screen.ids.timer.text = '00:00'
        self.i_timer = Clock.schedule_interval(callback=self.timer, timeout=1)
        self.ORDER = list(range(0, 15))
        self.correct_board = self.ORDER[:]
        self.correct_board.remove(0)
        self.correct_board.append(15)
        self.correct_board.append(0)
        self.correct_board.reverse()
        random.shuffle(self.ORDER)
        while not self.is_solvable():
            random.shuffle(self.ORDER)
        self.fix = self.ORDER[:]
        self.GigaRandom(self.fix)

    def switch_screen(self, screen):

        self.screen.current = screen
        self.i_timer.cancel()
        if screen == 'game':
            self.i_timer.cancel()
            self.new_game()

    def timer(self,cloak):
        self.tick += 1
        print(self.tick)
        min = self.tick // 60
        sec = self.tick - min * 60
        self.time = f'{min if min > 9 else "0" + str(min)}:{sec if sec > 9 else "0" + str(sec)}'
        app.screen.ids.timer.text = self.time


app = GameApp()
app.run()