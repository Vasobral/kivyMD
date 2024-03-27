from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import *
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivy.utils import get_color_from_hex, get_hex_from_color


size_line=40
type_edit="ellipse"
count = 1


class Holst(Image):
    def on_touch_down(self, touch):
        global count,x1,y1,x2,y2 #глобальные чтобы были доступны во всей функции

        if count == 1: #для проверки какое нажатие первое а какое второе
            x1 = touch.x
            y1 = touch.y
            count += 1
        elif count == 2:
            x2 = touch.x
            y2 = touch.y

            count += 1

        try:
            with self.canvas:
                if x1 and x2 and y1 and y2 > 0: #это для того чтобы при сбросе координат он автоматом не нарисовал с 0 координаты
                    s = get_color_from_hex(app.config.get('Pick','color')) #получаю цвет с конфиг файла и конвертация из hex в rgba

                    if app.type_edit == "line" and self.collide_point(touch.x + size_line / 2, touch.y + size_line / 2):#хз для чего но я оставил
                        if(app.config.get('Pick','mode')=='figure' and app.config.get('Pick','clear')=='false'): #для того чтобы сразу не рисовать в 3-х режимах
                            Color(s[0], s[1], s[2], s[3]) #тут задаю ранее полученый цвет(цвет хранится в массиве поэтому просто индексами)
                            Ellipse(
                                pos=[((x1+x2)/2)-((x2-x1)/2), ((y1+y2)/2)-((y2-y1)/2)],  #тут просто вычисляется центр между двумя нажатиями с учётом погрешности
                                size=[x2-x1, y2-y1], #это размер                         #дрочь в рисовании что киви рисует не точно по курсору а чуть выше
                                segments = 5  #у элипса есть параметр сегменты дефол это 180 типо элипс состоит из треугольников
                            )
                            x1, x2, y1, y2 = 0, 0, 0, 0  #сброс координат чтоб поновой нарисовать
                            count = 1
                        elif(app.config.get('Pick','mode')=='pen' and app.config.get('Pick','clear')=='false'):#для того чтобы сразу не рисовать в 3-х режимах
                            Color(s[0], s[1], s[2], s[3])
                            touch.ud["line"]=Line(
                                points=[touch.x-size_line/4,touch.y-size_line/4],
                                width=size_line/2
                            )
                        elif (app.config.get('Pick', 'clear') == 'true'):#для того чтобы сразу не рисовать в 3-х режимах
                            Color(255,255,255,1)#это белый цвет задаётся чтобы сделать типо ластика
                            touch.ud["line"] = Line(
                                points=[touch.x - size_line / 4, touch.y - size_line / 4],
                                width=size_line / 2
                            )



        except:
            pass

    def on_touch_move(self, touch):
        try:
            with self.canvas:
                if(app.config.get('Pick','clear')=='true'): #тут проверка на режим ластика или кисти
                    Color(255, 255, 255, 1)
                elif(app.config.get('Pick','clear')=='false'):
                    s = get_color_from_hex(app.config.get('Pick','color'))
                    Color(s[0], s[1], s[2], s[3])
                if app.type_edit == "line" and self.collide_point(touch.x+size_line/2,touch.y+size_line/2):
                    touch.ud["line"].points+=[touch.x-size_line/4,touch.y-size_line/4]


        except:
            pass


class IRightContainer(IRightBodyTouch, MDAnchorLayout):  #что-то из змейки для нормального вида в настройках по идеи
    adaptive_height = True

class DSC(MDGridLayout): #тоже хз что но пусть будет
    pass

class MyappApp(MDApp):
    def switch_screen(self, screen):
        global count, x1, y1, x2, y2     #тут я сбрасываю координаты при смене экрана
        self.screen.ids.sm.current = screen #сборс нужен так как он запоминал координаты когда я жал на кнопки в ТопАбаре
        x1, x2, y1, y2 = 0, 0, 0, 0
        count = 1

    def build_config(self, config): #это для создания конфиг файла с ним очень удобно передавать значения в другие классы и функции
        config.setdefaults(         #после написания этой функции конфиг файл сам появится после одного запуска программы
            'Pick', {
                'color':'#000000ff',
                'mode': 'figure',
                'clear':'false'

            }
        )

    def switch_mode(self, btn):  #тут логика свитч кнопки и как раз записываю новые данные в конфиг от куда потом я беру данные для проверки
        if btn.active:
            self.config.set('Pick', 'mode', 'figure')
            self.config.set('Pick', 'clear', 'false')
        else:
            self.config.set('Pick', 'mode', 'pen')
            self.config.set('Pick', 'clear', 'false')
        self.config.write()


    def clear_line(self):  #логика ластика просто при нажатии я меняю данные в конфиге
        self.config.set('Pick', 'clear', 'true')
        self.config.write()

    def show_dialog_color(self): #функциия для диалог окна
        if not self.dialog:
            color =  ['#ff0000ff',  #все мои цвета в hex формате
                      '#800080ff',
                      '#ffff00ff',
                      '#008000ff',
                      '#000000ff',
                      '#d2691eff',
                      '#00ffffff',
                      '#008080ff',
                      '#0000ffff',
                      '#ff4500ff',
                      '#c71585ff',
                      ]


            content = DSC()   #хз что он пусть будет
            for item in color: #спавн кнопок со всеми цветми в диалог окне
                btn = MDFloatingActionButton(
                    md_bg_color=item  #задний фон кнопок

                )
                btn.bind(on_press = self.switch_color) #логика кнопки


                print(get_hex_from_color(btn.md_bg_color))  #это я просто проверял как работает можно спокойно удалить


                content.add_widget(btn) #хз что но думаю оно обязательно
            self.dialog=MDDialog(  #это отображения диалог окна
                title='Выберите цвет',
                type='custom',
                content_cls=content #хз что но пусть будет
            )
            self.dialog.open()


    def switch_color(self,btn): #для проверки на какую кнопку нажали

        color = None
        match get_hex_from_color(btn.md_bg_color): #тут получаю цвет кнопки при нажатии и конвертирую в hex формат
            case '#ff0000ff':                     #тут думаю понятно что находит одинаковое и присвает значение
                color = '#ff0000ff'

            case '#800080ff':
                color = '#800080ff'

            case '#ffff00ff':
                color = '#ffff00ff'

            case '#008000ff':
                color = '#008000ff'

            case '#000000ff':
                color = '#000000ff'

            case '#d2691eff':
                color = '#d2691eff'

            case '#00ffffff':
                color = '#00ffffff'

            case '#008080ff':
                color = '#008080ff'

            case '#0000ffff':
                color = '#0000ffff'

            case '#ff4500ff':
                color = '#ff4500ff'

            case '#c71585ff':
                color = '#c71585ff'

        self.config.set('Pick','color',color) #заношу полученое значение в конфиг файл
        self.config.write()
        self.screen.ids.color_btn.md_bg_color = btn.md_bg_color #это насколько я понял чтобы предать в ui.kv задний фон кнопки
        self.dialog.dismiss() #хз что но надо
        self.dialog=None      #хз что но надо

    def clear_canvas(self): #это очистка всего холста
        self.screen.ids.holst.canvas.clear()

    def build(self):
        self.type_edit = 'line' #хз что но оставил
        self.screen=Builder.load_file('ui.kv')
        self.dialog = None

        self.config.set('Pick', 'clear', 'false') #это поидеи чтобы при запуске небыл сразу выбран ластик, но помоему оно криво работает
        self.config.write()
        return self.screen

app = MyappApp()
app.run()