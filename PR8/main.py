from kivy.config import Config
Config.set("graphics", "width", 700)
Config.set("graphics", "height", 700)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

from kivymd.uix.card import MDCard



class CSnackbar(BaseSnackbar):
    icon = StringProperty(None)
    text = StringProperty(None)
    color = ListProperty(None)

class Content(BoxLayout):
    pass

class DSC(MDGridLayout):
    pass

class MD3Card(MDCard):
    text = StringProperty()


class IRightContainer(IRightBodyTouch, MDAnchorLayout):
    adaptive_height = True

class GameApp(MDApp):
    def pro(self):
        return self.screen.ids
    def textcheck(self):
        self.count = 0
        file = open('text','r',encoding='utf-8')
        for line in file:
            if self.count < 3:
                self.screen.ids.box.add_widget(
                    MD3Card(

                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style="filled",
                        text=line,
                        md_bg_color="#373e4d",
                        shadow_softness=12,
                        shadow_offset=(0, 2),
                    )

                )
            elif self.count == 3:
                self.screen.ids.box2.add_widget(
                    MD3Card(

                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style="filled",
                        text=line,
                        md_bg_color="#373e4d",
                        shadow_softness=12,
                        shadow_offset=(0, 2),
                    )

                )
            elif 7 > self.count >= 4:
                self.screen.ids.box3.add_widget(
                    MD3Card(

                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style="filled",
                        text=line,
                        md_bg_color="#373e4d",
                        shadow_softness=12,
                        shadow_offset=(0, 2),
                    )

                )
            elif self.count == 7:
                self.screen.ids.box4.add_widget(
                    MD3Card(

                        line_color=(0.2, 0.2, 0.2, 0.8),
                        style="filled",
                        text=line,
                        md_bg_color="#373e4d",
                        shadow_softness=12,
                        shadow_offset=(0, 2),
                    )

                )
            self.count+=1

        file.close()

    def textadd(self):
        file = open('text','w',encoding='utf-8')
        file.write(f'Фамилия: {self.pro().t_sname.text}\nИмя: {self.pro().t_name.text}\n')
        if self.pro().loh.active == True:
            file.write(f'Отчество: Нет\n')
        else:
            file.write(f'Отчество: {self.pro().t_mname.text}\n')
        file.write(f'Организация: {self.pro().t_org.text}\nТовар: {self.pro().t_tov.text}\nОписание: {self.pro().t_opstov.text}\n')
        if self.pro().da.active == True:
            file.write(f'Товар краденый\n')
        else:
            file.write(f'Товар не краденый\n')
        file.write(f'Вид оплаты: {self.config.get("App", "hren")}\n')
        file.close()
        self.notifi()

    def notifi(self):
        notify = CSnackbar(
            text='Анкета создана',
            icon='account-tie-hat',
            snackbar_x=10,
            snackbar_y=10,
            color=[0, 1, 0, 1]
        )

        notify.size_hint_x = ((Window.width - 20) / Window.width)
        notify.open()


    def netpapi(self):
        if self.screen.ids.loh.active==True:
            self.screen.ids.t_mname.disabled = True
        else:
            self.screen.ids.t_mname.disabled = False

    def switch_dead(self,result):
        pass
        # self.dialog.dismiss()
        # self.dialog=None
        #
        # match result:
        #     case 'main':
        #         self.switch_screen('main')
        #
        #     case 'game':
        #         self.switch_screen('game')
        #         self.start()


    def show_dialog_dead(self,t):
        pass
        # if not self.dialog:
        #     self.dialog=MDDialog(
        #         title=f'{t} Вы играли на сложности {self.diff}, время игры: {self.screen.ids.timer.text}, всего раундов {self.log}',
        #         content_cls=Content(),
        #         type="custom",
        #         buttons = [
        #             MDFlatButton(
        #                 text='Menu',
        #                 theme_text_color='Custom',
        #                 text_color=self.theme_cls.accent_color,
        #                 on_press=lambda x:  self.switch_dead('main')
        #         ),
        #             MDFlatButton(
        #                 text='Заново',
        #                 theme_text_color='Custom',
        #                 text_color=self.theme_cls.accent_color,
        #                 on_press=lambda x: self.switch_dead('game')
        #             ),
        #             MDFlatButton(
        #                 text='Сохранить результат',
        #                 theme_text_color='Custom',
        #                 text_color=self.theme_cls.accent_color,
        #                 on_press=lambda x: self.msh_send(self.dialog.content_cls.ids.p_name.text, self.log, self.screen.ids.timer.text)
        #             ),
        #
        #         ],
        #
        #     )
        #
        #
        #
        # self.dialog.open()


    def switch_hren(self, hren):
        self.screen.ids.drop_hren.set_item(hren)
        self.config.set('App', 'hren', hren)
        self.config.write()
        self.drop_hren.dismiss()

    def build_config(self, config):
        config.setdefaults(
            'App', {
                'hren':'QIWI'
            }
        )

    def switch_screen(self, screen):
        self.screen.ids.sm.current = screen
        match screen:
            case 'main':
                self.screen.ids.nav.title = 'Главное меню'
            case 'create':
                self.screen.ids.nav.title = 'Создание анкеты'
            case 'check':
                self.screen.ids.nav.title = 'Просмотр анкеты'
                self.textcheck()

    def build(self):
        self.screen = Builder.load_file('ui.kv')


        self.screen.ids['cd'] = MD3Card


        self.drop_hren = MDDropdownMenu(
            caller=self.screen.ids.drop_hren,
            items=[
                {
                    'viewclass': 'OneLineListItem',
                    'text': hren,
                    'on_release': lambda x=hren: self.switch_hren(x)
                } for hren in  ['Наличные',
                                'Сбер',
                                'ВТБ',
                                'QIWI',
                                'Натурой',
                                ]
            ],
            width_mult=2,
            position='center'
        )
        return self.screen


app = GameApp()
app.run()

