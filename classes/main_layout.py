from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from classes.tools import timer

Builder.load_string(

    """
<Tile>:
    canvas.before:
        Color:
            rgba: root.bg_color if root.bg_color else root.off_color
        Rectangle:
            pos: self.pos
            size: self.size

<MainLayout>
    orientation: "lr-tb"
    spacing: 1

    """
)


class Tile(BoxLayout):
    bg_color = ListProperty()
    _root = ObjectProperty()
    
    off_color = ListProperty([0,0,0,1])
    on_color = ListProperty([1,1,1,1])
    state = "off"

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if self.state=="off":
            self.set_on()
        return super().on_touch_move(touch)

    def set_on(self):
        self.bg_color = self.on_color
        self.state = "on"
    
    def set_off(self):
        self.bg_color= self.off_color
        self.state = "off"

class MainLayout(GridLayout):
    field_size = ListProperty([30,60])
    max_on_tiles = NumericProperty(3)
    min_on_tiles = NumericProperty(2)
    tiles_to_die = NumericProperty(3)
    speed = NumericProperty(0.3)

    _clock = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._make_layout)        

    def _make_layout(self, *args):
        self.cols = self.field_size[0]
        tile_count = self.field_size[0]* self.field_size[1]

        for x in range(tile_count):
            self.add_widget(Tile(
                _root = self
            ))

    def get_tile_location(self, location, tile):
        index = self.get_tile_index(tile)
        tiles_x = self.field_size[0]
        around_tiles = []
        total_count = self.field_size[0]*self.field_size[1]
        
        if location == "right":
            # on the right margin
            if index % tiles_x == 0 :
                tile_location = index + tiles_x-1
            else:
                tile_location = index - 1

        elif location == "left":
            # on the left margin
            if index % tiles_x == tiles_x-1:
                tile_location = index - tiles_x
            else:
                tile_location = index+1

        elif location == "top":
            # on top margin
            if total_count-tiles_x<=index<total_count  :
                tile_location = tiles_x-(total_count - index)
            else:
                tile_location = index + tiles_x

        elif location == "bottom":
            # on the bottom margin
            if  0<=index<tiles_x :
                tile_location = total_count - 1  - (tiles_x-(index+1)) 
            else:
                tile_location = index - tiles_x 
        return self.get_tile_by_index(tile_location)

    def get_tile_by_index(self, index):
        return self.children[index]

    def get_tile_index(self, tile):
        return self.children.index(tile)

    def get_all_tiles(self):
        on = [x for x in self.children if x.state=="on"]
        tiles_list = []
        for x in on:
            tiles_list.extend([x for x in self.get_around_tiles(x) if x not in tiles_list])
        tiles_list.extend(on)
        return tiles_list

    def get_around_tiles(self, tile):
        top = self.get_tile_location("top", tile)
        bottom = self.get_tile_location("bottom", tile)
        right = self.get_tile_location("right", tile)
        left = self.get_tile_location("left", tile)
        top_left = self.get_tile_location("left", top)
        top_right = self.get_tile_location("right", top)
        bottom_left = self.get_tile_location("left", bottom)
        bottom_right = self.get_tile_location("right", bottom)
        return [top_left, top, top_right, right, bottom_right, bottom, bottom_left, left]

    def count_on_tiles(self, tile_list):
        on_list = [x for x in tile_list if x.state=="on"]
        return on_list

    def start_rules(self, *args):
        all_tiles = self.get_all_tiles()
        recipe_for_next = {"on":[], "off": []}
        for tile in all_tiles:
            around_tiles = self.get_around_tiles(tile)
            on_tiles = len(self.count_on_tiles(around_tiles))

            # checking rule 1
            if tile.state == "on":
                if on_tiles==self.max_on_tiles or on_tiles==self.min_on_tiles:
                    recipe_for_next["on"].append(tile)
                
                # rule 3
                else:
                    recipe_for_next["off"].append(tile)


            # rule two
            elif tile.state=="off":
                if on_tiles==3:
                    recipe_for_next["on"].append(tile)

        self.apply_recipe(recipe_for_next)

    def apply_recipe(self, recipe):
        to_be_on = recipe["on"]
        to_be_off = recipe["off"]
        
        for on_tile in to_be_on:
            on_tile.set_on()

        for off_tile in to_be_off:
            off_tile.set_off()

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        self.start()
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.reset()
            return True
        self.pause()
        return super().on_touch_down(touch)

    def start(self):
        self._clock = Clock.schedule_interval(self.start_rules, self.speed)        

    def pause(self):
        if not self._clock:
            return
        self._clock.cancel()

    def reset(self):
        self.pause()
        tiles = self.get_all_tiles()
        for tile in tiles:
            # if tile.state=="on":
            tile.set_off()