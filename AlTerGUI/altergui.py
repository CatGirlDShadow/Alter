import re
import time
from kivy.clock import Clock
from selenium.webdriver.firefox.options import Options
import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd_extensions.akivymd.uix.datepicker import AKDatePicker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    RoundedRectangularElevationBehavior,
)

# Window.fullscreen = True
Window.size = (1920, 1080)
# Window.maximize()


KV = '''
ScreenManager:
    ENTERScreen:
    OMSScreen:
    MOSScreen:
    OMSLoged:
    Loading:
<ENTERScreen>:
    name: 'enter'
    email: email_input
    password: text_field
    Image:
        source: 'bg.png'
        allow_stretch: True
        keep_ratio: False
    RelativeLayout:
        Image:
            source: 'alter.png'
            pos_hint: {'center_x': 0.5, 'center_y': .9}
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .65}
            size_hint: .2, .4
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDLabel:
                    text: "Войти через [color=1560db]EMIAS[/color]:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Логин"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(30)
                    helper_text_mode: "persistent"
                    size_hint: 1, .20
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .50}
                    mode: "fill"
                    icon_left: "key-variant"
                MDTextButton:
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: dp(30)
                    size_hint: .8, .17
                    pos_hint: {'center_x': .5, 'center_y': .20}
                    bold: True
                    on_press: root.check()
                    Image:
                        source: 'emias.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 362, 65
        MDSeparator:
            pos_hint: {'center_x': .435, 'center_y': .415}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255
        MDLabel:
            text: "[color=#808080]ИЛИ[/color]"
            bold: True
            markup: True
            font_name: 'roboto'
            pos_hint: {'center_x': .5, 'center_y': .415}
            halign: 'center'
        MDSeparator:
            pos_hint: {'center_x': .565, 'center_y': .415}
            size_hint_x: .1
            color: 128/255, 128/255, 128/255
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .27}
            size_hint: .2, .20
            MDRelativeLayout:
                orientation: 'horizontal'
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .30}
                    font_size: dp(25)
                    on_release: root.mos()
                    Image:
                        source: 'mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 358, 60
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .70}
                    font_size: dp(25)
                    on_release: root.oms()
                    Image:
                        source: 'oms.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 362, 65
                    
                
                    
    
<OMSScreen>:
    bdate: bdate
    policy: policy
    name: 'oms'
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .65}
            size_hint: .2, .4
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDLabel:
                    text: "Вход по полису ОМС:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: policy
                    hint_text: "Номер полиса"
                    mode: "fill"
                    max_text_length: 16
                    min_text_length: 16
                    font_size: dp(30)
                    input_filter: 'int'
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint: 1, .20
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "Например, 7100 0000 0000 0000"
                    icon_left: "account-details"
                MDTextButton:
                    size_hint: 1, .45
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    font_size: dp(25)
                    on_release: root.datepicker()
                MDTextField:
                    id: bdate
                    hint_text: "Дата Рождения"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, .20
                    disabled: True
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    readonly: True
                    icon_left: "account-details"
                MDFillRoundFlatButton:
                    text: "Войти"
                    ripple_color: app.theme_cls.primary_color
                    font_name: 'roboto'
                    font_size: 45
                    size_hint: .8, .1
                    md_bg_color: 0/255, 106/255, 240/255
                    pos_hint: {'center_x': .5, 'center_y': .25}
                    bold: True
                    on_release: root.omslogin()
                MDLabel:
                    text: "[color=#808080]Авторизируясь по полису[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .10}
                MDLabel:
                    text: "[color=#808080]будет доступен не полный функционал:[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .06}
                MDIconButton:
                    icon: "help"
                    pos_hint: {'center_x': .87, 'center_y': .075}
                    md_bg_color: 0/255, 106/255, 240/255
                    theme_icon_color: "Custom"
                    icon_color: 1,1,1,1
                    on_release: root.show_alert_dialog_info()
        
<MOSScreen>:
    name: 'mos'
    bdatemos: bdatemos
    policy: policy
    email: email_input
    password: text_field
    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True 
    MDFillRoundFlatButton:
        text: "На экран авторизации"
        pos_hint: {'center_x': .1, 'center_y': .92}
        font_name: 'roboto'
        font_size: dp(30)
        size_hint_y: .1
        md_bg_color: 0/255, 106/255, 240/255
        on_press: root.back()
        ripple_color: 1, 0, 0, 0.1
        bold: True
    RelativeLayout:
        id: omsrefresh
        MDCard:
            orientation: "vertical"
            elevation: 4
            shadow_radius: 6
            shadow_offset: 0, 2
            pos_hint: {'center_x': 0.5, 'center_y': .50}
            size_hint: .2, .7
            RelativeLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                MDTextField:
                    id: policy
                    hint_text: "Номер полиса(необязательно)"
                    mode: "fill"
                    max_text_length: 16
                    font_size: dp(30)
                    input_filter: 'int'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "Например, 7100 0000 0000 0000"
                    icon_left: "account-details"
                MDTextButton:
                    size_hint: 1, .1
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .35}
                    font_size: dp(25)
                    on_release: root.datepicker()
                MDTextField:
                    id: bdatemos
                    hint_text: "Дата Рождения(необязательно)"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .35}
                    disabled: True
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    readonly: True
                    icon_left: "account-details"
                MDLabel:
                    text: "[color=#808080]Без полиса и даты рождения [/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .10}
                MDLabel:
                    text: "[color=#808080]будет доступен не весь функционал:[/color]"
                    bold: True
                    markup: True
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .07}
                MDLabel:
                    text: "Войти через MOS.RU:"
                    bold: True
                    markup: True
                    font_size: dp(30)
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .958}
                    halign: 'center'
                MDTextField:
                    id: email_input
                    hint_text: "Телефон, электронная почта или СНИЛС"
                    mode: "fill"
                    font_size: dp(30)
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    helper_text: "mymail@mail.ru"
                    icon_left: "account-badge"
                MDTextField:
                    id: text_field
                    hint_text: "Пароль"
                    password: True
                    font_size: dp(30)
                    helper_text_mode: "persistent"
                    font_name: 'roboto'
                    pos_hint: {'center_x': .5, 'center_y': .65}
                    mode: "fill"
                    icon_left: "key-variant"
                MDTextButton:
                    size_hint: .8, .17
                    halign: 'center'
                    pos_hint: {'center_x': .5, 'center_y': .20}
                    font_size: dp(25)
                    on_release: root.check()
                    Image:
                        source: 'mos.png'
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        size: 358, 60
                MDIconButton:
                    icon: "help"
                    pos_hint: {'center_x': .85, 'center_y': .088}
                    md_bg_color: 0/255, 106/255, 240/255
                    theme_icon_color: "Custom"
                    icon_color: 1,1,1,1
                    on_release: root.show_alert_dialog()

<OMSLoged>:
    name: 'loged'
    MDFillRoundFlatButton:
        id: authname
        bold: True
        markup: True
        icon_color: 1, 0,0,1
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .92}
        font_size: dp(30)
        size_hint: .2,.05
        ripple_scale: 0
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        bold: True
    MDFillRoundFlatButton:
        id: curuser
        bold: True
        markup: True
        icon_color: 1, 0,0,1
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .86}
        font_size: dp(30)
        size_hint: .2,.05
        ripple_scale: 0
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        bold: True
    MDFillRoundFlatIconButton:
        text: "Выйти"
        bold: True
        icon: "delete"
        markup: True
        icon_color: 1, 0,0,1
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .80}
        font_size: dp(30)
        size_hint: .2,.05
        right_icon: "delete"
        md_bg_color: 0/255, 106/255, 240/255
        on_release: root.exits()
        ripple_color: 1, 1, 1, 1
        bold: True
    MDFillRoundFlatButton:
        id: full
        text: "Войти в полную версию"
        bold: True
        markup: True
        font_name: 'roboto'
        pos_hint: {'center_x': .9, 'center_y': .74}
        font_size: dp(30)
        size_hint: .2,.05
        md_bg_color: 0/255, 106/255, 240/255
        on_release: root.moslogin()
        ripple_color: 1, 1, 1, 1
        bold: True
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .35, 'center_y': .65}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("ЖАЛОБА")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Запись к врачу"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .35, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]Запись[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Просмотр записей[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Перенос записей[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Рецепты[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
            
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .65, 'center_y': .65}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("Запись")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Справки"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]COVID - 19[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Освобождение от[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .42}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]посещения учреждений[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .35}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Медосмотр[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Перенесенное заболевание[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .70, 'center_y': .20}
                halign: 'center'
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .35, 'center_y': .30}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("ЖАЛОБА")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Первичный прием"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .40, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]Простуда[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Болезни кожи AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Болезни горла AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Давление/Пульс/ЭКГ AI[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
    MDCard:
        orientation: "vertical"
        elevation: 4
        shadow_radius: 6
        shadow_offset: 0, 2
        pos_hint: {'center_x': .65, 'center_y': .30}
        size_hint: .2, .2
        ripple_behaviour: True
        on_release: print("Запись")
        RelativeLayout:
            orientation: 'vertical'
            size_hint: 1, 1
            MDFillRoundFlatButton:
                text: "Медкарта"
                bold: True
                markup: True
                icon_color: 1, 0,0,1
                font_name: 'roboto'
                pos_hint: {'center_x': .35, 'center_y': .82}
                font_size: dp(30)
                size_hint: .2,.05
                ripple_scale: 0
                right_icon: "delete"
                md_bg_color: 0/255, 106/255, 240/255
                bold: True
            MDLabel:
                text: "[color=#808080]История визитов[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Результаты исследований[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .40}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Результаты анализова[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .25, 'center_y': .20}
                halign: 'center'
            MDLabel:
                text: "[color=#808080]Поиск отклонений[/color]"
                bold: True
                markup: True
                font_name: 'roboto'
                pos_hint: {'center_x': .75, 'center_y': .20}
                halign: 'center'
        
<Loading>:
    name: "load"
    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        active: True 
        
<Item>
    id: mobiledialog
    orientation: "horizontal"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDTextField:
        id: verif1
        helper_text_mode: "persistent"
        font_name: 'roboto'
        on_text: verif2.focus = True
        size_hint: .1, .5
        max_text_length: 1
        pos_hint: {'center_x': .10, 'center_y': .65}
        mode: "fill"
    MDTextField:
        id: verif2
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif3.focus = True
        pos_hint: {'center_x': .28, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif3
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif4.focus = True
        pos_hint: {'center_x': .46, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif4
        helper_text_mode: "persistent"
        font_name: 'roboto'
        size_hint: .1, .5
        on_text: verif5.focus = True
        pos_hint: {'center_x': .64, 'center_y': .65}
        mode: "fill"
        max_text_length: 1
    MDTextField:
        id: verif5
        helper_text_mode: "persistent"
        font_name: 'roboto'
        max_text_length: 1
        size_hint: .1, .5
        pos_hint: {'center_x': .82, 'center_y': .65}
        mode: "fill"

        
'''


class Item(RelativeLayout):
    pass


class ENTERScreen(Screen):
    def check(self):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if self.email.text != "" and re.match(pattern, self.email.text) is not None:
            self.email.helper_text_color_normal = 'white'
            self.email.helper_text_color_focus = 'white'
            self.email.helper_text = ""
            if len(self.password.text) >= 8:
                self.password.helper_text_color_normal = 'white'
                self.password.helper_text_color_focus = 'white'
                # вход в emias по логину паролю
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = 'red'
                self.password.helper_text_color_focus = 'red'
        else:
            self.email.helper_text = "Введите корректный Email!"
            self.email.helper_text_color_normal = 'red'
            self.email.helper_text_color_focus = 'red'

    def oms(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = 'oms'

    def mos(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = 'mos'

    pass


class OMSScreen(Screen):
    dialog = None
    dialogs = None
    global result

    def back(self):
        self.bdate.text = ""
        self.policy.text = ""
        self.policy.helper_text = "Например, 7100 0000 0000 0000"
        self.manager.current = 'enter'

    def datepicker(self):
        self.date = AKDatePicker(callback=self.callback, opposite_colors='ffffff')
        self.date.open()

    def callback(self, date):
        global day, month, year
        try:
            year = str(date.year)
            if len(str(date.day)) > 1:
                day = str(date.day)
            else:
                day = "0" + str(date.day)
            if len(str(date.month)) > 1:
                month = str(date.month)
            else:
                month = "0" + str(date.month)
            self.bdate.text = day + "." + month + "." + year
        except:
            None

    def omsfunc(self, policy, day, month, year):
        t = threading.Thread(target=self.open_omslogin, args=[policy, day, month, year], daemon=True)
        t.start()

    def open_omslogin(self, policy, day, month, year):
        global result, curuserid
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        with webdriver.Firefox(executable_path="C:\\Users\\PCWORK\Desktop\\alter\AlterGUI\\geckodriver.exe" ,options=firefox_options) as driver:
            driver.get("https://emias.info/")
            driver.implicitly_wait(30)
            police_input = driver.find_element(By.NAME, 'policy')
            police_input.send_keys(policy)
            day_input = driver.find_element(By.NAME, 'day')
            day_input.send_keys(day)
            month_input = driver.find_element(By.NAME, 'month')
            month_input.send_keys(month)
            year_input = driver.find_element(By.NAME, 'year')
            year_input.send_keys(year)
            login_button = driver.find_element(By.XPATH,
                                               "/html/body/div[2]/main/div/div[2]/div/div/div/div/form/button").click()
            element_present = EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div'))
            page = WebDriverWait(driver, 10).until(element_present)
            try:
                check = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div[1]/div[1]/a[1]").click()
                element_present = EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]'))
                page = WebDriverWait(driver, 10).until(element_present)
                error = driver.find_element(By.XPATH,
                                            '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]').text
                result = 1
                driver.quit()
            except:
                result = 0
                curuserid = driver.find_element(By.XPATH,
                                                '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div').text
                driver.quit()

    def omslogin(self):
        def checkglobal(*args):
            global curuserid, result
            if result == None:
                None
            elif result == 1:
                result = None
                self.manager.current = "oms"
                self.show_alert_dialog()
                Clock.unschedule(clocks)
            else:
                self.manager.current = "loged"
                self.manager.get_screen('loged').ids.authname.text = "Полис:"
                self.manager.get_screen('loged').ids.curuser.text = curuserid
                Clock.unschedule(clocks)
                result = None

        if len(self.policy.text) < 16 or len(self.policy.text) > 16:
            self.policy.helper_text = "Некорректный полис"
            self.policy.helper_text_color_normal = 'red'
            self.policy.helper_text_color_focus = 'red'
        elif self.bdate.text != "":
            self.policy.helper_text = ""
            self.omsfunc(self.policy.text, day, month, year)
            self.manager.current = "load"
            clocks = Clock.schedule_interval(checkglobal, 2)

        else:
            self.bdate.helper_text = "Введите дату"
            self.bdate.helper_text_color_normal = 'red'
            self.bdate.helper_text_color_focus = 'red'


    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Пациент не найден",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()

    def show_alert_dialog_info(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                text="При входе только по ОМС вам будет не доступно: первичный осмотр с использованием AI, анализ медкарты и т.д. Будет доступно: Запись по направлению, запись к врачу, рецепты, перенос. Чтобы воспользоваться полной версией, войдите через mos.ru",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogs.dismiss()
                    )
                ],
            )
        self.dialogs.open()

    pass


class MOSScreen(Screen):
    dialogs = None
    dialog = None
    dialogerror = None
    dialogerror1 = None
    mobiles = None

    def back(self):
        self.email.text = ""
        self.password.text = ""
        self.bdatemos.text = ""
        self.policy.text = ""
        self.policy.helper_text = "Например, 7100 0000 0000 0000"
        self.bdatemos.text = ""
        self.manager.current = 'enter'

    def datepicker(self):
        self.date = AKDatePicker(callback=self.callback, opposite_colors='ffffff')
        self.date.open()

    def callback(self, date):
        global day, month, year
        try:
            year = str(date.year)
            if len(str(date.day)) > 1:
                day = str(date.day)
            else:
                day = "0" + str(date.day)
            if len(str(date.month)) > 1:
                month = str(date.month)
            else:
                month = "0" + str(date.month)
            self.bdatemos.text = day + "." + month + "." + year
        except:
            None

    def show_alert_dialog(self):
        if not self.dialogs:
            self.dialogs = MDDialog(
                text="Без полиса и даты рождения вам будет не доступно: запись по направлению, запись к врачу ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogs.dismiss()
                    )
                ],
            )
        self.dialogs.open()

    def error_dialog(self):
        if not self.dialogerror:
            self.dialogerror = MDDialog(
                text="Введен некорректный логин или пароль. Телефон может быть введен в любом формате, например, +79991234567. СНИЛС должен быть указан в виде последовательности цифр через дефисы или без разделителей. Электронная почта должна содержать символ @. ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogerror.dismiss()
                    )
                ],
            )
        self.dialogerror.open()

    def error_dialog1(self):
        if not self.dialogerror1:
            self.dialogerror1 = MDDialog(
                text="Введен неверный полис ОМС или дата рождения ",
                buttons=[
                    MDFillRoundFlatButton(
                        text="ОК",
                        on_release=lambda _: self.dialogerror1.dismiss()
                    )
                ],
            )
        self.dialogerror1.open()

    def mobile(self):
        def use_input(obj):
            global verifcode
            if self.mobiles.content_cls.ids.verif1.text == "" or self.mobiles.content_cls.ids.verif2.text == "" or self.mobiles.content_cls.ids.verif3.text == "" or self.mobiles.content_cls.ids.verif4.text == "" or self.mobiles.content_cls.ids.verif5.text == "" or len(
                    self.mobiles.content_cls.ids.verif1.text + self.mobiles.content_cls.ids.verif2.text + self.mobiles.content_cls.ids.verif3.text + self.mobiles.content_cls.ids.verif4.text + self.mobiles.content_cls.ids.verif5.text) > 5:
                None
            else:
                verifcode = self.mobiles.content_cls.ids.verif1.text + self.mobiles.content_cls.ids.verif2.text + self.mobiles.content_cls.ids.verif3.text + self.mobiles.content_cls.ids.verif4.text + self.mobiles.content_cls.ids.verif5.text
                self.mobiles.content_cls.ids.verif1.text = ""
                self.mobiles.content_cls.ids.verif2.text = ""
                self.mobiles.content_cls.ids.verif3.text = ""
                self.mobiles.content_cls.ids.verif4.text = ""
                self.mobiles.content_cls.ids.verif5.text = ""
                self.mobiles.dismiss()
                self.manager.current = "load"

        if not self.mobiles:
            self.mobiles = MDDialog(
                title="Введите СМС КОД",
                type="custom",
                auto_dismiss=False,
                content_cls=Item(),
                buttons=[
                    MDFillRoundFlatButton(
                        text="Ввести",
                        on_release=use_input

                    )
                ],
            )
        self.mobiles.open()

    def mosfunc(self, login, password):
        t = threading.Thread(target=self.open_moslogin, args=[login, password], daemon=True)
        if not t.is_alive():
            t.start()

    def mosfuncpol(self, login, password, policy, day, year, month):
        t = threading.Thread(target=self.open_mosloginpol, args=[login, password, policy, day, year, month],daemon=True)
        if not t.is_alive():
            t.start()

    def open_moslogin(self, login, password):
        global result, verifcode, curuserid
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("window_size=1920, 1080")
        with webdriver.Firefox(executable_path="C:\\Users\\PCWORK\Desktop\\alter\AlterGUI\\geckodriver.exe", options=firefox_options) as driver:
            driver.get("https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "login")))
            loginmos = driver.find_element(By.NAME, 'login')
            loginmos.send_keys(login)
            passwordmos = driver.find_element(By.NAME, 'password')
            passwordmos.send_keys(password)
            login_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
            try:
                error = driver.find_element(By.XPATH,"/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
                result = 0
                driver.quit()
            except:
                result = 1
                while True:
                    if verifcode == None:
                        None
                    else:
                        elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "otp_input")))
                        usercode = driver.find_element(By.ID, 'otp_input')
                        usercode.send_keys(verifcode)
                        userid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]")))
                        curuserid = driver.find_element(By.XPATH,
                                                        "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
                        result = 2
                        break
                        driver.quit()

    def open_mosloginpol(self, login, password, policy, day, year, month):
        global result, curuserid, polic
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        with webdriver.Firefox(executable_path="C:\\Users\\PCWORK\Desktop\\alter\AlterGUI\\geckodriver.exe", options=firefox_options) as driver:
            driver.get("https://emias.info/")
            driver.implicitly_wait(30)
            police_input = driver.find_element(By.NAME, 'policy')
            police_input.send_keys(policy)
            day_input = driver.find_element(By.NAME, 'day')
            day_input.send_keys(day)
            month_input = driver.find_element(By.NAME, 'month')
            month_input.send_keys(month)
            year_input = driver.find_element(By.NAME, 'year')
            year_input.send_keys(year)
            login_button = driver.find_element(By.XPATH,
                                               "/html/body/div[2]/main/div/div[2]/div/div/div/div/form/button").click()
            element_present = EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div'))
            page = WebDriverWait(driver, 20).until(element_present)
            try:
                check = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div[1]/div[1]/a[1]").click()
                element_present = EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]'))
                page = WebDriverWait(driver, 10).until(element_present)
                error = driver.find_element(By.XPATH,
                                            '/html/body/div[2]/main/div/div[2]/div[2]/div/div[2]/div/div[3]').text
                result = 1
                driver.quit()
            except:
                polic = driver.find_element(By.XPATH,
                                            '/html/body/div[2]/header/div/div[2]/div[2]/div/button/div/div').text
                driver.get("https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type%3Doffline%26client_id%3Dlk.emias.mos.ru%26scope%3Dopenid%2Bprofile%2Bcontacts%26redirect_uri%3Dhttps%3A%2F%2Flk.emias.mos.ru%2Fauth")
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "login")))
                loginmos = driver.find_element(By.NAME, 'login')
                loginmos.send_keys(login)
                passwordmos = driver.find_element(By.NAME, 'password')
                passwordmos.send_keys(password)
                login_mos = driver.find_element(By.XPATH,"/html/body/div[1]/main/section/div/div[2]/div/form/button").click()
                try:
                    error = driver.find_element(By.XPATH,
                                                "/html/body/div[1]/main/section/div/div[2]/div/div[2]/blockquote/p/a").text
                    result = 0
                    driver.quit()
                except:
                    result = 22
                    while True:
                        if verifcode == None:
                            None
                        else:
                            elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "otp_input")))
                            usercode = driver.find_element(By.ID, 'otp_input')
                            usercode.send_keys(verifcode)
                            curuserid = driver.find_element(By.XPATH,
                                                            "/html/body/div[1]/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/span[1]").text
                            result = "вошел"
                            break
                            driver.quit()

    def check(self):
        global login, password, year, month, day

        def checkglobal(*args):
            global curuserid, result, polic
            if result == None:
                None
            elif result == 1:
                result = None
                self.error_dialog1()
                self.manager.current = "mos"
                Clock.unschedule(clocks)
            elif result == 0:
                result = None
                self.error_dialog()
                Clock.unschedule(clocks)
            elif result == 22:
                self.manager.current = "mos"
                self.mobile()
                result = None
            else:
                self.manager.current = "loged"
                self.manager.get_screen('loged').ids.authname.text = "Полис:" + polic
                self.manager.get_screen('loged').ids.curuser.text = curuserid
                self.email.text = ""
                self.password.text = ""
                self.bdatemos.text = ""
                result = None
                Clock.unschedule(vclocks)

        def checkglobals(*args):
            global curuserid, result, polic
            if result == None:
                None
            elif result == 0:
                self.error_dialog()
                self.manager.current = "mos"
                result = None
                Clock.unschedule(clocks)
            elif result == 1:
                self.manager.current = "mos"
                self.mobile()
                result = None
            else: 
                self.manager.current = "loged"
                self.manager.get_screen('loged').ids.authname.text = "Пользователь: "
                self.manager.get_screen('loged').ids.curuser.text = "Пользователь: " + curuserid
                self.email.text = ""
                self.password.text = ""
                self.bdatemos.text = ""
                result = None
                Clock.unschedule(clocks)

        if self.email.text != "":
            self.email.helper_text_color_normal = 'white'
            self.email.helper_text_color_focus = 'white'
            self.email.helper_text = ""
            if len(self.password.text) >= 8:
                self.password.helper_text_color_normal = 'white'
                self.password.helper_text_color_focus = 'white'
                if self.policy.text == "" and self.bdatemos.text == "":
                    login = self.email.text
                    password = self.password.text
                    self.manager.current = "load"
                    self.mosfunc(login, password)
                    clocks = Clock.schedule_interval(checkglobals, 2)

                elif self.policy.text != "" or self.bdatemos.text != "":
                    if len(self.policy.text) < 16 or len(self.policy.text) > 16:
                        self.policy.helper_text = "Некорректный полис"
                        self.policy.helper_text_color_normal = 'red'
                        self.policy.helper_text_color_focus = 'red'
                    elif self.bdatemos.text == "":
                        self.bdatemos.helper_text = "Введите дату"
                        self.bdatemos.helper_text_color_normal = 'red'
                        self.bdatemos.helper_text_color_focus = 'red'
                        self.policy.helper_text = ""
                    else:
                        login = self.email.text
                        password = self.password.text
                        policy = self.policy.text
                        self.mosfuncpol(login, password, policy, day, year, month)
                        self.manager.current = "load"
                        vclocks = Clock.schedule_interval(checkglobal, 2)


            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = 'red'
                self.password.helper_text_color_focus = 'red'
        else:
            self.email.helper_text = "Введите телефон, электронную почта или СНИЛС "
            self.email.helper_text_color_normal = 'red'
            self.email.helper_text_color_focus = 'red'


class OMSLoged(Screen):
    def moslogin(self):
        self.manager.current = 'omsmos'

    def exits(self):
        self.manager.get_screen('oms').ids.policy.text = ""
        self.manager.get_screen('oms').ids.bdate.text = ""
        self.manager.current = 'enter'
        global day, year, month, verifcode, login, password, result, polic
        day = None
        year = None
        month = None
        verifcode = None
        login = None
        password = None
        result = None
        polic = None

    pass

class Loading(Screen):
    pass

class AlterApp(MDApp):
    def build(self):
        global day
        global year
        global month, verifcode, login, password, result, curuserid, polic
        day = None
        year = None
        month = None
        verifcode = None
        login = None
        password = None
        result = None
        polic = None
        sm = ScreenManager()
        sm.add_widget(ENTERScreen(name='enter'))
        sm.add_widget(OMSScreen(name="oms"))
        sm.add_widget(MOSScreen(name="mos"))
        sm.add_widget(OMSLoged(name="loged"))
        sm.add_widget(Loading(name="load"))
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


AlterApp().run()
# 5494499745000410
