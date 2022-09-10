from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from pathlib import Path

class KVLoadDialog:
    def __init__(self, path='',title='Open file', filter = ['*.json'], on_load_callback = None):
        self.filter = filter
        if path:
            self.path = path
        else:
            self.path = str(Path.cwd())

        self.on_load_callback = on_load_callback
        self.popup = Popup(title=title, content=self.create_popup_content(), auto_dismiss=False)

    def on_cancel(self, instance):
        self.popup.dismiss()

    def on_load(self, file_selection):
        if not (file_selection):
            return
        path_file_selection = Path(file_selection[0])
        if not (path_file_selection.is_file()):
            return

        self.popup.dismiss()
        if self.on_load_callback:
            self.on_load_callback(file_selection[0])


    def on_file_selection(self):
        print('sel')

    def create_popup_content(self):
        layout = BoxLayout(padding=5, orientation="vertical")

        #why not working???
        filechooser = FileChooserListView(on_selection=self.on_file_selection)
        filechooser.path = self.path
        filechooser.filters = self.filter
        layout.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=None, height=30)
        layout.add_widget(btn_layout)

        cancel_btn = Button(text='Cancel', on_release=self.on_cancel)
        btn_layout.add_widget(cancel_btn)

        load_btn = Button(text='Load', on_release= lambda _: self.on_load(filechooser.selection) )
        btn_layout.add_widget(load_btn)

        return layout

    def show_dialog(self):
        self.popup.open()
