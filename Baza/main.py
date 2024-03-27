from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.transition import MDSwapTransition


class CrashApp(MDApp):

    def switch_screen(self, screen): #функция перехода
        self.screen.ids.sm.current = screen

    def build(self):
        self.screen = Builder.load_file('ui.kv')
        self.screen.ids.sm.transition = MDSwapTransition() #анимация перехода
        return self.screen





app = CrashApp()
app.run()