import pygame
import kivy
import Daddbf_functions as dbf

from datetime import date, datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.adapters.listadapter import ListAdapter

kivy.require('1.9.1')

Builder.load_string('''
#: import Checkbox kivy.uix.checkbox
#: import ListView kivy.uix.listview.ListView
#: import ListAdapter kivy.adapters.listadapter.ListAdapter
#: import ListItemButton kivy.uix.listview.ListItemButton

<SpinnerOption>:
    text_size: self.width, None
    valign: 'middle'
    halign: 'center'

<SucessPopup>:
    size_hint: .7, .7
    auto_dismiss: False
    title: "Sucess"
    BoxLayout:
        orientation: "vertical"
        ScrollView:
            Label:
                text: root.label_text
                font_size: 16
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        Button:
            text: "Close"
            on_press: root.dismiss()

<FailPopup>:
    size_hint: .7, .7
    auto_dismiss: False
    title: "Failure"
    BoxLayout:
        orientation: "vertical"
        ScrollView:
            Label:
                text: root.label_text
                font_size: 16
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        Button:
            text: "Close"
            on_press: root.dismiss()

<InfoPopup>:
    auto_dismiss: False
    title: "Resultados"
    BoxLayout:
        orientation: "vertical"
        ScrollView:
            Label:
                text: root.label_text
                font_size: 16
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        Button:
            size_hint_y: 0.2
            text: "Close"
            on_press: root.on_press_dismiss()

<ScreenOne>:
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 0, 0, 0, 1
            text: "Tela Inicial"
        Button:
            text: "Tela de Insercao"
            on_press:
                root.manager.current = 'screen_two'
        Button:
            text: "Tela de Pesquisa"
            on_press:
                root.manager.current = 'screen_three'
        Button:
            text: "Apagar/Alterar"
            on_press:
                root.manager.current = 'screen_five'

        Button:
            text: "Tela 4"
            on_press:
                root.manager.current = 'screen_four'

<ScreenTwo>:
    spinner_input: input_spinner
    spin_input: input_spin
    other_ins_input: input_ins_other
    service_ins_input: input_ins_service
    comment_ins_input: input_ins_comment
    dia_input: input_dia
    mes_input: input_mes
    ano_input: input_ano
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Lancha"
            Spinner:
                text: "..."
                values: ["Vera Cruz", "Catarina Paraguaçu", "Bahia Express", "Joanna Angélica", "Anitta Garibaldi", "Maria Quitéria", "Vitória Régia", "Mestre Pequeno", "Senhor do Bonfim", "Maria Rita", "Outra"]
                id: input_spinner
            TextInput:
                id: input_ins_other
                hint_text: "Digite aqui se sua opcao foi 'Outra'"
                multiline: False

        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "40dp"
            Spinner:
                text: "Data Atual"
                size: self.texture_size
                values: ["Data Atual", "Outra Data"]
                id: input_spin
            Label:
                color: 0, 0, 0, 1
                text: "Dia"
            TextInput:
                id: input_dia
                input_filter: 'int'
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Mês"
            TextInput:
                id: input_mes
                input_filter: 'int'
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Ano"
            TextInput:
                id: input_ano
                input_filter: 'int'
                multiline: False

        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Servico"
                multiline: True
            TextInput:
                id: input_ins_service
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Comentario"
            TextInput:
                id: input_ins_comment
                multiline: True
        BoxLayout:
            Button:
                text: "Adicionar"
                size: self.texture_size
                on_press: root.InsertButton()

<ScreenThree>:
    dia_input: input_dia
    mes_input: input_mes
    ano_input: input_ano
    lancha_input: input_lancha
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Dia"
            TextInput:
                id: input_dia
                input_filter: 'int'
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Mes"
            TextInput:
                id: input_mes
                input_filter: 'int'
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Ano"
            TextInput:
                id: input_ano
                input_filter: 'int'
                multiline: False
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "40dp"
            Label:
                color: 0, 0, 0, 1
                text: "Lancha"
            TextInput:
                id: input_lancha
                multiline: False
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: "40dp"
            Label:
                color: 0, 0, 0, 1
                text: "Pesquisa por lancha"
            CheckBox:
                group: "search_opt"
                value: root.opt1
                on_active: root.search_lancha(self, self.active)
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Pesquisa por data"
            CheckBox:
                group: "search_opt"
                value: root.opt2
                on_active: root.search_data(self, self.active)

<ScreenFour>:
    dia_text_input: dia
    mes_text_input: mes
    ano_text_input: ano
    entry_list: entry_list
    on_pre_enter:
        root.reset_list()

    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Dia"
            TextInput:
                id: dia
                input_filter: "int"
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Mes"
            TextInput:
                id: mes
                input_filter: "int"
                multiline: False
            Label:
                color: 0, 0, 0, 1
                text: "Ano"
            TextInput:
                id: ano
                input_filter: "int"
                multiline: False
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            Button:
                text: "Mostrar Detalhes"
                size: self.texture_size
                on_press: root.entry_details()
            Button:
                text: "Deletar Entrada"
                size: self.texture_size
                on_press: root.delete_entry()
        ListView:
            id: entry_list
            adapter:
                ListAdapter(data=root.list, cls = ListItemButton)

<ScreenFive>:
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        Button:
            text: "Enviar pro email"
            size: self.texture_size
            on_press: root.sendTE()
''')

class SucessPopup(Popup):
    label_text = StringProperty('')

class FailPopup(Popup):
    label_text = StringProperty('')

class InfoPopup(Popup):
    label_text = StringProperty('')

    def on_press_dismiss(self):
        self.label_text = ''
        self.dismiss()

# tela inicial
class ScreenOne(Screen):
    dbf.InitTable()

# tela para inserir dados
class ScreenTwo(Screen):
    lancha = StringProperty('')
    servico = StringProperty('')
    comentario = StringProperty('')
    dia = StringProperty('')
    mes = StringProperty('')
    ano = StringProperty('')

    def InsertButton(self):
        if self.spin_input.text == 'Data Atual':
            day = date.today()
        else:
            self.dia = '' + self.dia_input.text
            self.mes = '' + self.mes_input.text
            self.ano = '' + self.ano_input.text
            day = datetime.date(day=int(self.dia), month=int(self.mes), year=int(self.ano))
        if self.spinner_input.text == 'Outra':
            self.lancha = '' + self.other_ins_input.text.lower()
        else:
            self.lancha = '' + self.spinner_input.text
        self.servico = '' + self.service_ins_input.text.lower()
        self.comentario = '' + self.comment_ins_input.text
        try:
            dbf.InsertEntry(self.lancha, self.servico, day, self.comentario)
            popup = SucessPopup()
            popup.label_text = 'Entrada foi inserida na database'
            popup.open()
        except:
            popup = FailPopup()
            popup.label_text = 'Erro'
            popup.open()
        self.other_ins_input.text = ''
        self.service_ins_input.text = ''
        self.comment_ins_input.text = ''

class ScreenThree(Screen):
    opt1 = ObjectProperty(False)
    opt2 = ObjectProperty(False)
    dia = StringProperty('')
    mes = StringProperty('')
    ano = StringProperty('')
    lancha = StringProperty('')
    info = StringProperty('')

    def search_lancha(self, instance, value):
        self.lancha = '' + self.lancha_input.text
        entradas = dbf.SearchLancha(self.lancha.lower())
        self.info = ''
        for entrada in entradas:
            self.info = self.info + 'Lancha: '+entrada[0]+'\n'+'Servico: '+entrada[1]+'\n'+'Data: '+str(entrada[2])+'\n'+'Comentario: '+entrada[3]+'\n\n'
        try:
            thepopup = InfoPopup()
            thepopup.label_text = self.info
            thepopup.open()
            self.lancha_input.text = ''
            self.dia_input = ''
            self.mes_input = ''
            self.ano_input = ''
        except:
            poopup = FailPopup
            poopup.label_text = 'Error'
            poopup.open()

    def search_data(self, instance, value):
        self.dia = self.dia_input.text
        self.mes = self.mes_input.text
        self.ano = self.ano_input.text
        entradas = dbf.SearchDate(int(self.dia), int(self.mes), int(self.ano))
        self.info = ''
        for entrada in entradas:
            self.info = self.info + 'Lancha: '+entrada[0]+'\n'+'Servico: '+entrada[1]+'\n'+'Data: '+str(entrada[2])+'\n'+'Comentario: '+entrada[3]+'\n\n'
        try:
            thepopup = InfoPopup()
            thepopup.label_text = self.info
            thepopup.open()
            self.lancha_input.text = ''
            self.dia_input.text = ''
            self.mes_input.text = ''
            self.ano_input.text = ''
        except:
            poopup = FailPopup()
            poopup.label_text = 'Error'
            poopup.open()

class ScreenFour(Screen):
    entradas = dbf.SearchLancha('')
    lista = []
    for entrada in entradas:
        lista.append(entrada[0]+' '+ str(entrada[2]))
    list = ListProperty(lista)
    entry = ObjectProperty()
    dia_text_input = ObjectProperty()
    mes_text_input = ObjectProperty()
    ano_text_input = ObjectProperty()

    def reset_list(self):
        self.entradas = dbf.SearchLancha('')
        self.lista.clear()
        for entrada in self.entradas:
            self.lista.append(entrada[0] + ' ' + str(entrada[2]))
        self.entry_list.adapter.data = self.lista
        self.entry_list._trigger_reset_populate()

    def entry_details(self):
        if self.entry_list.adapter.selection:
            selection = self.entry_list.adapter.selection[0].text
            print(selection)
            for entry in self.entradas:
                if (entry[0]+' '+str(entry[2])) == selection:
                    popup = InfoPopup()
                    popup.label_text = entry[1]
                    popup.open()
                    break
            self.entry_list._trigger_reset_populate()
            self.dia_text_input.text = ''
            self.mes_text_input.text = ''
            self.ano_text_input.text = ''

    def delete_entry(self):#está ok, por enquanto
        if self.entry_list.adapter.selection:
            selection = self.entry_list.adapter.selection[0].text
            print(selection)
            for entry in self.entradas:
                if (entry[0]+' '+str(entry[2])) == selection:
                    dbf.DeleteEntry(entry[0], entry[2])
                    self.entry_list.adapter.data.remove(selection)
                    break
            self.entry_list._trigger_reset_populate()
            self.dia_text_input.text = ''
            self.mes_text_input.text = ''
            self.ano_text_input.text = ''

class ScreenFive(Screen):
    #envia as entradas pro email, e deleta tudo que seja de pelo menos 7 dias atras
    def sendTE(self):
        dbf.SendToEmail()
        dbf.DeleteAfterLimit()

class TheApp(App):
    manager = ObjectProperty()

    screen_manager = ScreenManager()
    screen_manager.add_widget(ScreenOne(name="screen_one"))
    screen_manager.add_widget(ScreenTwo(name="screen_two"))
    screen_manager.add_widget(ScreenThree(name="screen_three"))
    screen_manager.add_widget(ScreenFour(name="screen_four"))
    screen_manager.add_widget(ScreenFive(name="screen_five"))


    def build(self):
        Window.clearcolor = (0.5, 0.5, 0.5, 1)
        Window.softinput_mode = 'below_target'
        Window.bind(on_keyboard=self.onBackBtn)
        return self.screen_manager

    def onBackBtn(self, window, key, *args):
        if key == 27:
            if not self.screen_manager.current == 'screen_one':
                self.screen_manager.current = 'screen_one'
                return True
            else:
                return False

theapp = TheApp()
theapp.run()