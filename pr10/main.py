from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.snackbar import BaseSnackbar
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
import pymysql
from pymysql.cursors import DictCursor



class Content(BoxLayout):
    pass


class CSnackbar(BaseSnackbar):
    icon = StringProperty(None)
    text = StringProperty(None)
    color = ListProperty(None)

class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()

class Example(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Orange'
        self.screen = Builder.load_file('ui.kv')

    def build(self):
        self.dialog=None
        self.dialog2 = None

        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='rating',
            cursorclass=DictCursor
        )
        if not self.conn:
            self.stop()
        return self.screen

    def add_notify(self, types: str, text: str):

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

    def show_dialog_one(self):
        if not self.dialog:
            self.dialog=MDDialog(
                title=f'Добавление',
                content_cls=Content(),
                type="custom",
                buttons = [
                    MDFlatButton(
                        text='Потвердить',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x:  self.addnote()

                ),
                    MDFlatButton(
                        text='Закрыть',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x: self.dialog.dismiss()
                    ),
                ],

            )



        self.dialog.open()

    def hren(self,instance):
        self.hren1 = instance.text.split('.')
        self.hren2 = self.hren1[0].split('№')
        with self.conn.cursor() as cursor:
            cursor.execute(f'select name, text from note where id={int(self.hren2[1])}')
            result = cursor.fetchall()

        for i in result:
            self.dialog2.content_cls.ids.p_name.text = i['name']
            self.dialog2.content_cls.ids.p_text.text = i['text']


    def show_dialog_two(self,instance):
        if not self.dialog2:
            self.dialog2=MDDialog(
                title=f'Редактирование',
                content_cls=Content(),
                type="custom",
                buttons = [
                    MDFlatButton(
                        text='Потвердить',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x:  self.renote(instance)

                ),
                    MDFlatButton(
                        text='Закрыть',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.accent_color,
                        on_press=lambda x: self.dialog2.dismiss()
                    ),
                ],

            )



        self.dialog2.open()

    def renote(self,instance):
        self.work1 = instance.text.split('.')
        self.work2 = self.work1[0].split('№')

        with self.conn.cursor() as cursor:
            cursor.execute(
                f'update note set `name`="{self.dialog2.content_cls.ids.p_name.text}",`text`="{self.dialog2.content_cls.ids.p_text.text}" where id="{int(self.work2[1])}"')




        self.refresh()
        self.add_notify('s', 'Заметка изменена')



        self.conn.commit()


    def addnote(self):
        with self.conn.cursor() as cursor:
            cursor.execute(f'insert into note (`name`, `text`) values'
                           f' ("{self.dialog.content_cls.ids.p_name.text}", "{self.dialog.content_cls.ids.p_text.text}")')
            self.refresh()
            self.add_notify('s', 'Заметка добавлена')
            self.conn.commit()



    def remove_item(self, instance):
        try:
            self.work1 = instance.text.split('.')
            self.work2= self.work1[0].split('№')
            print(self.work2[1])

            with self.conn.cursor() as cursor:
                cursor.execute(f'delete from note where id={self.work2[1]}')


            self.add_notify('s', 'Заметка удалена')
            self.refresh()
            self.screen.ids.md_list.remove_widget(instance)
        except Exception as error:
            self.add_notify('e', 'error')


    def refresh(self):
        self.conn.commit()
        self.screen.ids.md_list.clear_widgets()

        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM note')
            result = cursor.fetchall()
        for row in result:
            card = SwipeToDeleteItem(
                text=f"№{row['id']}. {row['name']}: {row['text']}"
            )
            self.screen.ids.md_list.add_widget(card)

    def on_start(self):
        self.count = 0
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM note')
            result = cursor.fetchall()
        for row in result:
            card = SwipeToDeleteItem(
                text=f"№{row['id']}. {row['name']}: {row['text']}"
            )
            self.screen.ids.md_list.add_widget(card)
            self.screen.ids[f'card{self.count}'] = card
            self.count+=1



    def test(self,instance):
        print(instance)

Example().run()