import ntsecuritycon
from kivymd.app import MDApp
from kivy.lang import Builder
import pymysql
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.snackbar import BaseSnackbar
from kivy.core.window import Window
from pymysql.cursors import DictCursor
from kivymd.uix.transition import MDSwapTransition
from hashlib import pbkdf2_hmac
from os import urandom
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatIconButton


class Message(MDCard):
    def __init__(self,login:str,msg:str,i:bool = False,*args,**kwargs):
        self.login=login
        self.msg=msg
        self.i =i
        super().__init__(*args,**kwargs)


class AddContent(MDBoxLayout):
    def __init__(self, name_f: str = '', desc_f: str = '', active_f: bool = False, edit: bool = False, *args, **kwargs):
        self.current = name_f
        self.name_f = name_f
        self.desc_f = desc_f
        self.active_f = active_f
        self.edit = edit
        super().__init__(*args, **kwargs)


class CSnackbar(BaseSnackbar):
    icon = StringProperty(None)
    text = StringProperty(None)
    color = ListProperty(None)

class ChatApp(MDApp):
    def build(self):
        self.conn = pymysql.connect(
            host='10.49.22.231',
            user='meat',
            password='meat',
            database='chat',
            cursorclass=DictCursor
        )
        if not self.conn:

            self.stop()
        self.prev_row = None
        self.screen = Builder.load_file('ui.kv')
        self.screen.transition = MDSwapTransition()
        self.user = {
            'id': self.config.get('Session', 'id'),
            'login': self.config.get('Session', 'login')
        }
        if not self.user['id'] != None:
            self.screen.current = 'login'
        table = MDDataTable(
            use_pagination=True,
            rows_num=5,
            check=True,
            pagination_menu_pos='center',
            column_data=[
                ('Имя', 60),
                ('Описание', 60),
                ('Активно', 60)
            ]
        )

        table.bind(on_row_press=self.on_row_press)
        self.theme_cls.primary_palette = 'Green'
        self.screen.ids.lt_table_chat.add_widget(table)
        self.refresh_table()
        self.dialog = MDDialog(
            title='Добавление записи',
            type='custom',
            content_cls=AddContent(),

        )
        return self.screen

    def on_row_press(self, table, row):
        if row.ids.check.active:
            row.ids.check.active = False
        else:
            if not self.prev_row is None:
                self.prev_row.ids.check.active = False
            row.ids.check.active = True
            self.prev_row = row



    def refresh_table(self):
        self.conn.commit()
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM chats')
            result = cursor.fetchall()

        self.screen.ids.lt_table_chat.children[0].row_data = []
        for row in result:
            self.screen.ids.lt_table_chat.children[0].add_row((
                row['name'],
                row['desc'],
                ('check-underline-circle' if row['active'] else 'check-underline-circle-outline',
                 [0,1,0,1] if row['active'] else [1,0,0,1],
                 'ON' if row['active'] else 'OFF')
            ))


    def del_row(self):
        table = self.screen.ids.lt_table_chat.children[0]
        row = table.get_row_checks()[0]
        self.prev_row.ids.check.active = False
        with self.conn.cursor() as cursor:
            cursor.execute(f'delete from chats where name = "{row[0]}"')
        self.conn.commit()
        self.refresh_table()


    def add_row(self, name, desc, active):
        try:
            if name and desc != '':
                with self.conn.cursor() as cursor:
                    cursor.execute(f'insert into chats (`name`, `desc`, `active`) values'
                                       f' ("{name}", "{desc}", {active})')
                    self.refresh_table()
                    self.add_notify('s', 'Чайт добавлен')
                    self.dialog.dismiss()
                    cnt = self.dialog.content_cls.ids
                    cnt.dl_name.text = ''
                    cnt.dl_desc.text = ''
                    cnt.dl_active.text = ''
                    cnt.dl_active.active = False

        except Exception as error:
            self.add_notify('e', 'error')

        self.conn.commit()
        self.refresh_table()

    def edit_row_dialog(self):
        row = self.screen.ids.lt_table_chat.children[0].get_row_checks()[0]

        self.dialog_e = MDDialog(
            title=f'Редактирование чата {row[0]}',
            type='custom',
            content_cls=AddContent(name_f=row[0],desc_f=row[1],active_f=bool(row[2]), edit=True)
        )
        self.dialog_e.open()


    def edit_row(self, name, desc, active, current):
        try:
            if name and desc != '':
                with self.conn.cursor() as cursor:
                    cursor.execute(f'update chats set `name`="{name}", `desc`="{desc}", `active`={active} where name="{current}"')
                    self.refresh_table()
                    self.add_notify('s', 'Чайт изменен')
                    self.dialog_e.dismiss()

        except Exception as error:
            self.add_notify('e', 'error')

        self.conn.commit()
        self.refresh_table()


    def refresh_chat(self):
        self.conn.commit()
        with self.conn.cursor() as cursor:
            cursor.execute(f'select count(*) as `count` from msg')
            result =  cursor.fetchone()
            count = result['count']
            cursor.execute(f'select users.login as login, msg.text as `msg` from msg,chats,users '
                           f'where users.id=msg.author and msg.chat=chats.id and msg.chat = {self.chat["id"]} limit {self.msg_count},{count-self.msg_count} ')
            result= cursor.fetchall()
            self.msg_count=count
            print(result)
        for msg in result:
            self.screen.ids.msg_box.add_widget(Message(login=msg['login'], msg=msg['msg']))
        self.screen.ids.msg_scroll.scroll_y=0


    def open_chat(self):
        self.msg_count = 0
        row = self.screen.ids.lt_table_chat.children[0].get_row_checks()[0]
        if row[2]=='OFF':
            self.add_notify('e', 'Чат не работат!')
            return
        with self.conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM chats  where name="{row[0]}"')
            self.chat = cursor.fetchone()
            if not self.chat['active']:
                self.add_notify('e', 'Чат не работат!')
                return
            self.screen.ids.sm_main.current='kuda'
            self.msg_refresh = Clock.schedule_interval(lambda x:self.refresh_chat(),1)


    def msh_send(self,msg:str):
        with self.conn.cursor() as cursor:
            cursor.execute(f'insert into msg(text, author, chat) value("{msg}",{self.user["id"]},{self.chat["id"]})')
        self.conn.commit()
        self.refresh_chat()



    def build_config(self, config):
        config.setdefaults(
            'Session', {
                'id': None,
                'login': None
            }
        )

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




    def login(self, login: str, password: str):
        with self.conn.cursor() as cursor:
            cursor.execute(f'select * from users where login="{login}"')
            result = cursor.fetchone()

            if not result:
                self.add_notify('e', 'Не правильное или то или другое')
                return
            else:
                password_old = result['password'].encode('latin1').decode('unicode-escape').encode('latin1')
                salt = password_old[:6]
                password = pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    salt,
                    10000,
                    16
                )
                if password_old[6:] == password:
                    self.config.set('Session', 'id', result['id'])
                    self.config.set('Session', 'login', result['login'])
                    self.config.write()
                    self.user = {
                        'id': self.config.get('Session', 'id'),
                        'login': self.config.get('Session', 'login')
                    }
                    self.screen.ids.pr_user.text = 'Пользователь: ' + login
                    self.add_notify('s', 'Я тебе доверяю')
                    self.screen.current = 'chat'
                else:
                    self.add_notify('e', 'Не правильное или то или другое')



    def change_password(self, old_password: str, new_password:str, rep_password: str):
        if new_password != rep_password:
            self.add_notify('e', 'Пароли не совпадают')
            return

        with self.conn.cursor() as cursor:
            cursor.execute(f'select * from users where id={self.user["id"]}')
            result = cursor.fetchone()
            db_password = self.str_to_bytes(result['password'])
            salt = db_password[0][:6]
            check_password = self.hash_password(old_password, db_password[0][:6])

            if check_password != db_password[6:]:
                self.add_notify('e', 'Неверный текущий пароль')
            else:
                salt = urandom(6)
            password = pbkdf2_hmac(
                'sha256',
                old_password.encode('utf-8'),
                salt,
                10000,
                16
            )
            password = str(salt + password).replace('\\','\\\\')
            cursor.execute(f'update users set password="{password}" where id={self.user["id"]}')
        self.conn.commit()
        self.add_notify('s', 'Пароль изменен')





    def reg(self, login: str, password1: str, password2: str):
        if password1 != password2:
            self.add_notify('e', 'Пароли не совпадают')
            return
        try:

            password = self.hash_password(password1, urandom(6))

            with self.conn.cursor() as cursos:

                cursos.execute(f'insert into  users (login, password) values ("{login}", "{password[1]}")')
            self.conn.commit()
            self.add_notify('s', 'Вы успешно зарегестрировались!')


        except:
            self.add_notify('e', 'Ошибка. Проверьте данные.')

    def logout(self):
        self.user = {'id': 'None', 'login': 'None'}
        self.config.set('Session', 'id', 'None')
        self.config.set('Session', 'login', 'None')
        self.config.write()
        self.screen.current = 'login'

    def list_chat(self):

        table = MDDataTable(
            column_data=[
                ("Имя", 30),
                ("Описание", 30),
                ("Активна", 30),
            ],
            # self.screen.ids.lt_table_chat.add_widget(table)
        )

    def hash_password(self, password: str, salt: bytes = None):

        if salt is None:
            salt = urandom(6)
        p_hash = salt + pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10000,
            16
        )

        p_sql = str(p_hash).replace('\\', '\\\\')[2:-1]
        return [p_hash, p_sql]

    def str_to_bytes(self, p_hash: str):
        return p_hash.encode('latin1').decode('unicode-escape').encode('latin1')





app = ChatApp()
app.run()
