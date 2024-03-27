from kivy.core.window import Window
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.snackbar import Snackbar
from configparser import ConfigParser
import time
from kivy.clock import Clock
import random

P = 0

EMPTY_SQUARE = 0


class Pole(MDGridLayout):

    def replace(self, x, y):
        global P


        text_x = self.children[x]
        text_y = self.children[y]
        self.children[x]=text_y
        self.children[y]=text_x
        P=y
        app.fix[x], app.fix[y] = app.fix[y], app.fix[x]
        if app.fix == app.correct_board:
            Snackbar(text="Ура победа...").open()
            app.switch_screen('main')
        print(app.fix)





    def sdvig(self, x):
        global P
        if (x=='up'):
            if P-4 >= 0:
                self.replace(P, P-4)

        if (x=='down'):
            if P + 4 <= 15:
                self.replace(P, P+4)
        if (x=='right'):
            if (P+1)%4!=0:
                self.replace(P, P+1)
        if (x=='left'):
            if P%4!=0:
                self.replace(P, P-1)




    def on_touch_down(self, touch):
        touch.ud["x"]=touch.x
        touch.ud["y"] = touch.y


    def on_touch_up(self, touch):
        x=touch.ud["x"]-touch.x
        y = touch.ud["y"] - touch.y
        if (abs(x)-abs(y)>0):
            if (x>0):
                self.sdvig("left")
            else:
                self.sdvig("right")
        else:
            if y>0:
                self.sdvig("down")
            else:
                self.sdvig("up")


class PR(MDApp):
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

    def switch_screen(self, screen: str):
        self.screen.ids.sm.current = screen
        if screen == 'game':
            self.start_time = time.time()
            self.clock_event = Clock.schedule_interval(self.update_time, 1.0 / 60.0)
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


            self.Random(self.fix)

        elif screen != 'game' and hasattr(self, 'clock_event'):
            self.clock_event.cancel()
            elapsed_time = time.time() - self.start_time
            if elapsed_time < self.best_time:
                self.best_time = elapsed_time
                config = ConfigParser()
                config.read('config.ini')
                if not config.has_section('BEST_TIME'):
                    config.add_section('BEST_TIME')
                config.set('BEST_TIME', 'time', str(elapsed_time))
                with open('config.ini', 'w') as config_file:
                    config.write(config_file)

            self.start_time = 0

    def update_time(self, nap):
        elapsed_time = time.time() - self.start_time
        self.screen.ids.time.text = f'Time: {elapsed_time:.2f}'

    def Random(self,a):

        a.remove(EMPTY_SQUARE)
        for i in range(14):
            self.screen.ids[f'm{i}'].text = str(a[i])


        self.screen.ids.m15.text=""
        self.fix.append(15)
        self.fix.append(0)
        self.fix.reverse()



    def Cheat(self):
        for i in range(15):
            self.screen.ids[f'm{i}'].text = str(i+1)



    def build(self):

        config = ConfigParser()
        config.read('config.ini')
        self.best_time = config.getfloat('BEST_TIME', 'time', fallback=float('inf'))
        Window.size = (400, 800)
        self.ORDER = list(range(1, 17))
        self.correct_board = self.ORDER[:]
        self.screen = Builder.load_file('ui.kv')
        self.screen.ids.bestTimeEver.text = f'Лучшее время: {self.best_time:.2f}'


        return self.screen


if __name__ == '__main__':
    app = PR()
    app.run()
