from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import BaseSnackbar
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty


class IRightContainer(IRightBodyTouch, MDAnchorLayout):
    adaptive_height = True

class CSnackbar(BaseSnackbar):
    icon = StringProperty(None)
    text = StringProperty(None)
    color = ListProperty(None)

class MyappApp(MDApp):
    def build(self):
        self.screen=Builder.load_file('ui.kv')
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
        return self.screen


    def switch_theme(self, x):
        if x == 'lt':
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.theme_style_switch_animation = True
            self.theme_cls.theme_style_switch_animation_duration = 0.8

        elif x =='dk':
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.theme_style_switch_animation = True
            self.theme_cls.theme_style_switch_animation_duration = 0.8


    def otenk(self,x):
        x=round(x)
        match x:
            case 1:
                self.theme_cls.primary_hue ="50"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 2:
                self.theme_cls.primary_hue ="100"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 3:
                self.theme_cls.primary_hue ="200"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 4:
                self.theme_cls.primary_hue ="300"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 5:
                self.theme_cls.primary_hue ="400"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 6:
                self.theme_cls.primary_hue ="500"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 7:
                self.theme_cls.primary_hue ="600"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 8:
                self.theme_cls.primary_hue ="700"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 9:
                self.theme_cls.primary_hue ="800"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")
            case 10:
                self.theme_cls.primary_hue ="900"
                self.theme_cls.primary_palette = "Blue"
                self.theme_cls.primary_palette = self.config.get("App","primary_palette")


    def add_notify(self, types: str, text: str):
        # cancel alert-circle check-circle
        match types:
            case 'e':
                icon = 'cancel'
                color = [1, 0, 0, 1]
            case 's':
                icon = 'check-circle'
                color = [0, 1, 0, 1]
            case _:
                icon = 'information'
                color = [1, 1, 0, 0]

        notify = CSnackbar(
            text=text,
            icon=icon,
            snackbar_x=10,
            snackbar_y=10,
            color=color
        )

        notify.size_hint_x = ((Window.width - 20) / Window.width)
        notify.open()


    def switch_screen(self, screen):
        global temp
        match screen:
            case 'second':
                try:
                    arr = self.screen.ids.text_f.text.split()
                    temp = self.screen.ids.f_s.value
                    s = 0
                    e = int(temp)
                    for i in range(int(temp)):
                        TextField = MDTextField(
                            hint_text=str(i),
                            mode='rectangle',
                            width=10,
                            text = f"{arr[s:e]}"
                        )
                        self.screen.ids.box.add_widget(TextField)

                        s = e
                        e +=e
                    for i in range(int(temp)):
                        self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace("'","")
                        self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace('[','')
                        self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace("]","")
                        self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace(",", " ")
                except Exception:
                    self.add_notify('e','Ошибка, возможно введены не числа через пробел')

        self.screen.ids.sm.current = screen


    def switch_palette(self, color):
        self.theme_cls.primary_palette = color
        self.config.set('App', 'primary_palette', color)
        self.config.write()
        self.drop_palette.dismiss()


    def build_config(self, config):
        config.setdefaults(
            'App', {
                'primary_palette': 'Orange',
            }
        )

    def minus(self):
        try:
            slide = self.screen.ids.s_s.value
            arr = []
            arr2 = []
            arr3 = []
            for i in reversed(range(int(temp))):
                arr = self.screen.ids.box.children[i].text.split()
                for j in range(len(arr)):
                    arr2.append(int(arr[j]))
            count = 0
            try:
                for i in arr2:
                    if count == int(slide):
                        break
                    if i < 0:
                        arr3.append(i)
                        count += 1
            except Exception:
                pass
            for i in arr3:
                arr2.remove(i)

            s = 0
            e = int(temp)
            for i in reversed(range(int(temp))):
                try:
                    self.screen.ids.box.children[i].text = f"{arr2[s:e]}"
                    s = e
                    e += e
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace('[', ' ')
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace("]", " ")
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace(",", " ")
                except Exception:
                    pass
        except Exception:
            self.add_notify('e','Уже всё удалено')

    def plus(self):
        try:
            slide = self.screen.ids.s_s.value
            arr=[]
            arr2=[]
            arr3=[]
            for i in reversed(range(int(temp))):
                arr = self.screen.ids.box.children[i].text.split()
                for j in range(len(arr)):
                    arr2.append(int(arr[j]))
            count =0
            try:
                for i in arr2:

                    if count == int(slide):
                        break
                    if i >= 0:

                        arr3.append(i)
                        count+=1
            except Exception:
                pass
            for i in arr3:
                arr2.remove(i)
            s = 0
            e = int(temp)
            for i in reversed(range(int(temp))):
                try:
                    self.screen.ids.box.children[i].text = f"{arr2[s:e]}"
                    s = e
                    e+=e
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace('[', ' ')
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace("]", " ")
                    self.screen.ids.box.children[i].text = self.screen.ids.box.children[i].text.replace(",", " ")
                except Exception:
                    pass
        except Exception:
            self.add_notify('e','Уже всё удалено')


app = MyappApp()
app.run()