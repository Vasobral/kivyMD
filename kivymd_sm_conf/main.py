from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.utils.asynckivy import start, sleep
from kivymd.uix.transition import MDSwapTransition
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from random import randrange
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivy.clock import Clock



class Snake:
    def __init__(self):
        self.body = [[1, 4], [1, 3], [1, 2], [1, 1]]
        self.speed = .5
        self.movement = 'up'
        self.eat_apple = 0
        self.DEBUG = False

    def move(self,clock):
        if not app.game.apple:
            app.game.apple = Apple()
            app.game.apple.refresh()
        current = app.game.snake.body[0]
        if not ((app.game.snake.movement) == 'right' and app.game.movement == 'left' or
                (app.game.snake.movement) == 'left' and app.game.movement == 'right' or
                (app.game.snake.movement) == 'up' and app.game.movement == 'down' or
                (app.game.snake.movement) == 'down' and app.game.movement == 'up'
        ):
            app.game.snake.movement = app.game.movement
        else:
            app.game.movement = app.game.snake.movement
        match app.game.snake.movement:
            case 'up':
                current = [current[0], current[1] + 1]
            case 'down':
                current = [current[0], current[1] - 1]
            case 'left':
                current = [current[0] - 1, current[1]]
            case 'right':
                current = [current[0] + 1, current[1]]
        autocannibalism = current in app.game.snake.body[:-1]
        match app.game.mode:
            case 'easy':

                masochist = False
                if current[0] == 0:
                    current[0] = app.game.size
                if current[1] == 0:
                    current[1] = app.game.size
                if current[0] > app.game.size:
                    current[0] = 1
                if current[1] > app.game.size:
                    current[1] = 1
            case 'hard':
                masochist = current[0] > app.game.size or current[1] > app.game.size or current[0] < 1 or \
                            current[1] < 1

        if app.game.apple.noun == app.game.snake.body[0]:
            app.game.apple = None
            app.game.snake.eat_apple += 1
            app.game.snake.speed -= 0.5 / (
                    app.game.size * app.game.size) / 2 if app.game.snake.speed > 0.08 else 0
            app.game.i_move.timeout = app.game.snake.speed
            eat = True
        else:
            eat = False

        if autocannibalism or masochist:
            app.game.stop()
            app.show_dialog_dead()
        else:
            if not eat:
                app.change_holst([app.game.snake.body[-1:][0][0] - 1, app.game.snake.body[-1:][0][1] - 1],
                                  [.8, .8, .8, 1])
                app.game.snake.body.remove(app.game.snake.body[-1:][0])

            app.game.snake.body.insert(0, current)
            app.change_holst([current[0] - 1, current[1] - 1], [1, 0, 0, 1])
        if self.DEBUG:
            print(
                f'Змея: body={app.game.snake.body}, move={app.game.snake.movement}, eat={app.game.snake.eat_apple}, apple={app.game.apple.noun if app.game.apple else None}')



class Apple:
    def __init__(self):
        while True:
            self.noun = [randrange(1, app.game.size, 1), randrange(1, app.game.size, 1)]
            if self.noun not in app.game.snake.body:
                break
    def refresh(self):
        app.change_holst([self.noun[0] - 1, self.noun[1] - 1], [0, 1, 0, 1])


class Game:
    def __init__(self):
        self.size = int(app.config.get('Game','size'))
        self.mode = app.config.get('Game','mode')
        self.width = None
        self.snake = Snake()
        self.apple = None
        self.status = False
        self.time = '00:00'
        self.tick = 0
        self.movement = 'up'
        self.i_timer =None
        self.i_move = None

    def start(self):
        self.status = True
        app.screen.ids.timer.icon = 'stop'
        app.screen.ids.holst.canvas.clear()
        app.create_holst()
        self.i_timer = Clock.schedule_interval(callback=self.timer, timeout=1)
        self.i_move = Clock.schedule_interval(callback=self.snake.move, timeout=self.snake.speed)
    def stop(self):
        app.screen.ids.timer.icon = 'play'
        self.status = False
        self.i_timer.cancel()
        self.i_move.cancel()
        self.tick = 0
        self.time = '00:00'


    def timer(self,clock):
        self.tick += 1
        min = self.tick // 60
        sec = self.tick - min * 60
        self.time = f'{min if min > 9 else "0" + str(min)}:{sec if sec > 9 else "0" + str(sec)}'
        app.screen.ids.timer.title = app.game.time




class DSC(MDGridLayout):
    pass



class Holst(Image):
    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y) and app.game.status:
            self.touch = [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.collide_point(touch.x,touch.y) and app.game.status:
            x_line = touch.x - self.touch[0]
            y_line = touch.y - self.touch[1]
            if abs(x_line) > abs(y_line):
                if x_line > 0:
                    app.game.movement = 'right'
                else:
                    app.game.movement = 'left'
            else:
                if y_line > 0:
                    app.game.movement = 'up'
                else:
                    app.game.movement = 'down'


class IRightContainer(IRightBodyTouch, MDAnchorLayout):
    adaptive_height = True


class CrashApp(MDApp):
    def change_holst(self, noun: [], color: []):
        with self.screen.ids.holst.canvas:
            Color(color[0], color[1], color[2], color[3])
            Rectangle(
                pos=[self.screen.ids.holst.pos[0] + 5 + (self.game.width + 5) * noun[0],
                     self.screen.ids.holst.pos[1] + 5 + (self.game.width + 5) * noun[1]],
                size=[self.game.width, self.game.width]
            )

    def create_holst(self):
        # self.screen.ids.holst.canvas.clear()
        self.game.width = self.screen.ids.holst.width - 5 * (self.game.size + 1)
        self.game.width = self.game.width / self.game.size
        for x in range(self.game.size):
            for y in range(self.game.size):
                self.change_holst([x, y], [.8, .8, .8, 1])
            for x in self.game.snake.body:
                self.change_holst([x[0] - 1, x[1] - 1], [1, 0, 0, 1])


    def engine(self):
        if self.game.status:
            self.game.stop()

        else:
            self.game = Game()
            self.game.start()


    def switch_dead(self,result):
        self.dialog.dismiss()
        self.dialog=None
        match result:
            case 'main':
                self.switch_screen('main')
            case 'restart':
                self.engine()


    def show_dialog_dead(self):
        if not self.dialog:
            self.dialog=MDDialog(
                title='Snake? Snaaaaaake !',
                text=f'Вы играли на сложности {self.game.mode} собрав {self.game.snake.eat_apple} яблок',
                buttons = [
                    MDFlatButton(
                        text='Menu',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x: self.switch_dead('main')
                ),
                    MDFlatButton(
                        text='Заново',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x: self.switch_dead('restart')
                    ),

                ]
            )
        self.dialog.open()

    def show_dialog_size(self):

        if not self.dialog:

            items = [{'icon':'l', 'size':'8'},
                     {'icon':'m', 'size':'12'},
                     {'icon':'s', 'size':'16'},
                     {'icon':'xl', 'size':'20'},
                     {'icon':'xs', 'size':'24'},
                     {'icon':'xxl', 'size':'28'},
                     {'icon':'xxs', 'size':'32'},
                     {'icon':'xxxl', 'size':'36'},

            ]
            content = DSC()
            for item in items:
                btn = MDFloatingActionButton(
                    icon='size-'+item['icon'],
                    md_bg_color=self.theme_cls.accent_color if item['size'] == self.config.get('Game','size') else [.8,.8,.8,1]
                )
                btn.bind(on_press = self.switch_size)
                content.add_widget(btn)
            self.dialog=MDDialog(
                title='Выберите размер поля',
                type='custom',
                content_cls=content
            )
        self.dialog.open()





    def switch_screen(self, screen):
        self.screen.ids.sm.current = screen

    def build_config(self, config):
        config.setdefaults(
            'App', {
                'theme_style': 'Light',
                'primary_palette': 'Orange'
            }
        )
        config.setdefaults(
            'Game', {
                'mode': 'hard',
                'size': '16',

            }
        )

    def switch_mode(self, btn):
        if btn.active:
            self.config.set('Game', 'mode', 'hard')
        else:
            self.config.set('Game', 'mode', 'easy')
        self.config.write()

    def switch_size(self,btn):
        size = None
        match btn.icon[5:]:
            case 'l':
                size = 8
            case 'm':
                size = 12
            case 's':
                size = 16
            case 'xl':
                size = 20
            case 'xs':
                size = 24
            case 'xxl':
                size = 28
            case 'xxs':
                size =32
            case 'xxxl':
                size = 36
        self.config.set('Game','size',size)
        self.config.write()
        self.screen.ids.size_btn.icon = btn.icon
        self.dialog.dismiss()
        self.dialog=None

    def switch_palette(self, color):
        self.theme_cls.primary_palette = color
        self.config.set('App', 'primary_palette', color)
        self.config.write()
        self.drop_palette.dismiss()

    def switch_theme(self, btn):
        if not btn.active:
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.set_clearcolor_by_theme_style('Light')
        else:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.set_clearcolor_by_theme_style('Dark')
        self.config.set('App', 'theme_style', self.theme_cls.theme_style)
        self.config.write()

    def build(self):
        self.game = Game()
        self.dialog = None
        self.item_size =[{'icon':'l', 'size':'8'},
                     {'icon':'m', 'size':'12'},
                     {'icon':'s', 'size':'16'},
                     {'icon':'xl', 'size':'20'},
                     {'icon':'xs', 'size':'24'},
                     {'icon':'xxl', 'size':'28'},
                     {'icon':'xxs', 'size':'32'},
                     {'icon':'xxxl', 'size':'36'},
            ]
        self.size_start=['size-'+item['icon'] for item in self.item_size if item['size']==self.config.get('Game','size')][0]
        self.screen = Builder.load_file('ui.kv')
        self.theme_cls.theme_style = self.config.get('App', 'theme_style')
        self.theme_cls.primary_palette = self.config.get('App', 'primary_palette')
        self.drop_palette = MDDropdownMenu(
            caller=self.screen.ids.drop_palette,
            items=[
                {
                    'viewclass': 'OneLineListItem',
                    'text': color,
                    'on_release': lambda x=color: self.switch_palette(x)
                } for color in ['Red',
                                'Pink',
                                'Purple',
                                'DeepPurple',
                                'Indigo',
                                'Blue',
                                'LightBlue',
                                'Cyan',
                                'Teal',
                                'Green',
                                'LightGreen',
                                'Lime',
                                'Yellow',
                                'Amber',
                                'Orange',
                                'DeepOrange',
                                'Brown',
                                'Gray',
                                'BlueGray'
                                ]
            ],
            width_mult=2,
            position='center'
        )
        self.screen.ids.sm.transition = MDSwapTransition()
        return self.screen


app = CrashApp()
app.run()
