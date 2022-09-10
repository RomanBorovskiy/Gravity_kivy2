import kivy
kivy.require('1.0.5')

from constants import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.logger import Logger
from kivy.clock import Clock
from planets import Planet, PlanetSystem
import numpy as np
from pathlib import Path
from kivy_load_dialog import KVLoadDialog




#---------------------------------------------------
class WtPlanet(Widget):
    """
    Widget for Planet object
    """

    planet = ObjectProperty()
    trace = ListProperty([])

    def __init__(self, **kwargs):
        super(WtPlanet, self).__init__(**kwargs)
        self.planet = kwargs['planet']

    def get_trace(self):
        if self.parent:
            root = App.get_running_app().root
            if root.show_traces:
                return self.trace

        return []

#---------------------------------------------------
class MainWindow(Widget):

    label_info = ObjectProperty()
    btn_start = ObjectProperty()
    space = ObjectProperty()
    scroll_view  = ObjectProperty()


    state = NumericProperty(0)
    show_axes = NumericProperty(0)
    show_traces = NumericProperty(0)

    ps = PlanetSystem()
    scale = NumericProperty(1)
    gl_scale = NumericProperty(1)

    count = 0
    draw_is_init = False
    #----------------------------
    def do_start_stop(self):
        if self.state == 0:
            self.btn_start.text = "PAUSE"
            self.state = 1
        else:
            self.btn_start.text = 'START'
            self.state = 0

    def do_load_dialog(self):
        def load_callback(filename):
            self.ps.load_json(filename)
            self.init_draw()

        KVLoadDialog(path = str(TEMPLATES_DIR), on_load_callback=load_callback).show_dialog()
    #----------------------------
    def scale_change(self, delta):
        if not delta:
            self.scale=1
            return

        self.scale += delta

        if self.scale>MAX_SCALE:
            self.scale=MAX_SCALE
        elif self.scale<MIN_SCALE:
            self.scale=MIN_SCALE

    #----------------------------
    def load_objects(self):
        #create demo list of planets

        def demo_load1():
            k=10
            self.ps.add_planet(Planet(name = 'SUN', position = np.array((0,0)), velocity = np.array((0,0)), size = 200, mass = 2557))
            self.ps.add_planet(Planet(name='MERCURY', position=np.array((58*k, 0)), velocity=np.array((0, 1)), size=4, mass=3.3, color=(0, 0, 1)))
            self.ps.add_planet(Planet(name='VENUS', position=np.array((108*k, 0)), velocity=np.array((0, 1)), size=9.5, mass=48.8, color=(0, 0, 1)))
            self.ps.add_planet(Planet(name='EARTH', position=np.array((149*k, 0)), velocity=np.array((0, 1)), size=10, mass=59.7, color = (0,0,1)))
            self.ps.add_planet(Planet(name='MARS', position=np.array((228*k, 0)), velocity=np.array((0, 1)), size=5.3, mass=6.4, color=(1, 0, 0)))
            self.ps.add_planet(Planet(name='JUPITER', position=np.array((778*k, 0)), velocity=np.array((0, 1)), size=50, mass=900, color=(0, 0, 1)))
            self.ps.add_planet(Planet(name='Halley', position=np.array((300*k, 220)), velocity=np.array((-1, -1.75)), size=5, mass=.01,
                                      color=(1, 0.5, 0.5)))
            #self.ps.save_to_json(filename='solar_system.json')

        def demo_load2():
            self.ps.add_planet(Planet(name='SUN_1', position=np.array((-50.1, 0)), velocity=np.array((.25, -1)), size=20, mass=130, color = (1,1,0)))
            self.ps.add_planet(Planet(name='SUN_2', position=np.array((50, 0)), velocity=np.array((-.25, 1)), size=20, mass=130, color=(0, 0, 1)))

        #use demo_load1 or demo_load2
        #demo_load1()
        demo_load2()
        self.log(f'Demo Load planets: {len(self.ps.planet_list)}')


    #----------------------------
    def init_draw(self):
        """
            for every Planet in planet_list create widget WTPlanet
        """
        self.space.clear_widgets()
        for obj in self.ps.planet_list:
            obj.object = WtPlanet(planet = obj)
            self.space.add_widget(obj.object)

        self.wt_planets_position_update(with_trace=True)
        self.info_update()

        self.draw_is_init = True
        self.log(f'Create Planets: {len(self.ps.planet_list)}')
    # ----------------------------
    def show_info_text(self, text=''):
        self.label_info.text = text

    def info_update(self):
        self.show_info_text(f' TIME: {str(self.count)} SCALE: {self.scale:.1f}')

    def log(self, text=''):
        Logger.info('GRAVITY: '+text)

    #----------------------------
    def update(self, dt):
        """
        Calling by clock for update planets positions
        """
        # if UI not ready yet
        if not self.space:
            return

        if not self.draw_is_init:
            self.init_draw()

        if self.state == 0:
            return

        self.ps.calc_new_positions()
        self.wt_planets_position_update()

        self.count+=1
        self.info_update()



    #----------------------------
    def wt_planets_position_update(self, with_trace=True):
        for obj in self.ps.planet_list:
            obj.object.pos = (int(obj.position[0]), int(obj.position[1]))

            if with_trace:
                obj.object.trace.append(list(obj.object.pos))
                if len(obj.object.trace)>MAX_TRACE:
                    obj.object.trace.pop(0)

    #----------------------------
    def wt_planets_clear_trace(self):
        for obj in self.ps.planet_list:
            obj.object.trace=[]

#---------------------------------------------------
class GravityApp(App):

    def build(self):
        gravity_app = MainWindow()
        gravity_app.load_objects()
        gravity_app.init_draw()
        Clock.schedule_interval(gravity_app.update, 1.0 / 60.0)
        return gravity_app

#---------------------------------------------------
if __name__ == '__main__':
    GravityApp().run()