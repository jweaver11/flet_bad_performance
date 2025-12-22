'''
The map class for all maps inside our story
Maps are widgets that have their own drawing canvas, and info display. they can contain nested sub maps as well.
'''

#TODO: 
# BLANK NO TEMPLATE MAPS EXIST AS WELL
# ADD DUPLICATE OPTION AS WELL
# Users can choose to create their image or use some default ones, or upload their own
# When hovering over a map, display it on the rail as well so we can see where new sub maps would

# THERES A MAP DISPLAY DUMMY, HB U CHECK THAT OUT!!!!!


import os
import json
import flet as ft
from models.widget import Widget
from models.views.story import Story
from handlers.verify_data import verify_data
from styles.snack_bar import Snack_Bar
from models.state import State
import flet.canvas as cv
from threading import Thread



class Canvas(Widget):
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        # Supported categories: World map, continent, region, ocean, country, city, dungeon, room, none.
        
        
        # Parent constructor
        super().__init__(
            title=title,           
            page=page,                         
            directory_path=directory_path, 
            story=story,
            data=data,  
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,
            {
                "tag": "canvas",
                
                "canvas_meta": dict,     # stores width/height used for the coords for resizing
                "canvas": list,          # Stores the lines data to storage so we can load it later
            },
        )

        # State tracking for canvas drawing info
        self.state: State = State()         # Used for our coordinates and how to apply things

        # Track last known canvas size to rescale drawings on resize
        self._last_canvas_size: tuple[float, float] | None = None

        self.canvas: cv.Canvas = cv.Canvas(
            content=ft.GestureDetector(
                on_pan_start=self.start_drawing,
                on_pan_update=self.is_drawing,
                on_pan_end=lambda e: self.save_canvas(),
                drag_interval=30,
                
            ),
            expand=True,
            on_resize=self.on_canvas_resize, resize_interval=20,
        )

        self.canvas_container: ft.Container = ft.Container(
            content=self.canvas,
            expand=True, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        )

        #self.information_display: Drawing_Information_Display = Drawing_Information_Display()
        #self.mini_widgets.append(self.information_display)
        
       
        # Load our drawing/display
        self.load_canvas()
        self.reload_widget()

    # Called on launch to load our drawing from data into our canvas
    def load_canvas(self):
        """Loads our drawing from our saved map drawing file."""

        lines = self.data.get('canvas', [])
        for line in lines:
            x1, y1, x2, y2, paint_settings = line
            self.canvas.shapes.append(
                cv.Line(
                    x1, y1, x2, y2,
                    ft.Paint(**paint_settings),
                )
            )

    
        
    # Called when we start drawing on the canvas
    async def start_drawing(self, e: ft.DragStartEvent):
        ''' Set our initial starting x and y coordinates for the line we're drawing '''
        self.state.x, self.state.y = e.local_x, e.local_y

    # Called when actively drawing on the canvas
    async def is_drawing(self, e: ft.DragUpdateEvent):
        ''' Creates our line to add to the canvas as we draw, and saves that lines data to self.state '''
        
        # Create our line using our previous x and y, the current x and y, and our brush settings.
        line = cv.Line(
            self.state.x, self.state.y, e.local_x, e.local_y,
            paint=ft.Paint(**self.story.data.get('paint_settings', {})),
        )

        # Add the line to our canvas so we can see it
        self.canvas.shapes.append(line)

        # After dragging canvas widget, it loses page reference and can't update
        try:
            self.canvas.update()
        except Exception as ex:
            self.p.update()
        

        # Store the shape so we can save it to data
        self.state.shapes.append((self.state.x, self.state.y, e.local_x, e.local_y, line.paint.__dict__))

        # Update our state x and y for the next segment
        self.state.x, self.state.y = e.local_x, e.local_y
        
        

    # Called when we release the mouse to stop drawing a line
    def save_canvas(self):
        """ Saves our lines to our canvas data for storage """
        
        # Add on to what we already have
        self.data['canvas'].extend(self.state.shapes)

        self.save_dict()

        # Clear the current state, otherwise it constantly grows and lags the program
        self.state.shapes.clear()


    def _rebuild_canvas_from_state(self) -> None:
        """Rebuild visible canvas shapes from self.state.shapes."""
        self.canvas.shapes.clear()
        for x1, y1, x2, y2 in self.state.shapes:
            self.canvas.shapes.append(
                cv.Line(x1, y1, x2, y2, paint=self.paint)
            )

        #self.p.update()
        self.canvas.update()

    # Called when the canvas control is resized
    async def on_canvas_resize(self, e: ft.ControlEvent):
        """Rescales stored drawing coordinates to match the new canvas size."""
        new_w = getattr(e, "width", None)
        new_h = getattr(e, "height", None)

        # Fallback if event doesn't expose width/height
        if not new_w or not new_h:
            new_w = getattr(self.canvas_container, "width", None)
            new_h = getattr(self.canvas_container, "height", None)

        if not new_w or not new_h:
            return

        # First size we learn: treat as baseline (no rescale yet)
        if self._last_canvas_size is None:
            self._last_canvas_size = (float(new_w), float(new_h))
            self.data["canvas_meta"] = {"w": float(new_w), "h": float(new_h)}
            return

        old_w, old_h = self._last_canvas_size
        if old_w <= 0 or old_h <= 0:
            self._last_canvas_size = (float(new_w), float(new_h))
            self.data["canvas_meta"] = {"w": float(new_w), "h": float(new_h)}
            return

        sx = float(new_w) / float(old_w)
        sy = float(new_h) / float(old_h)

        if sx == 1.0 and sy == 1.0:
            return

        # Scale all stored coords
        self.state.shapes = [
            (x1 * sx, y1 * sy, x2 * sx, y2 * sy)
            for (x1, y1, x2, y2) in self.state.shapes
        ]

        self._rebuild_canvas_from_state()

        # Update meta so future resizes and saves remain consistent
        self._last_canvas_size = (float(new_w), float(new_h))
        self.data["canvas_meta"] = {"w": float(new_w), "h": float(new_h)}

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):       
        ''' Rebuilds/reloads our map UI '''

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        self.body_container.content = self.canvas_container

        self._render_widget()
    


# Add notes to drawings, duhhh


# What a drawing should do on load:
# Load its normal widget data
# Load its drawing data (shapes, lines, etc) from its _canvas file
# resize_interval = 10