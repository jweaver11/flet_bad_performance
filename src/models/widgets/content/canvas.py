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
                "canvas": list,          # Stores our drawing data
                "canvas": {
                    'paths': list,
                    'points': list,
                },
            },
        )

        # State tracking for canvas drawing info
        self.state: State = State()         # Used for our coordinates and how to apply things
        self.min_segment_dist: float = 3.0

        # Track last known canvas size to rescale drawings on resize
        self._last_canvas_size: tuple[float, float] | None = None

        self.canvas: cv.Canvas = cv.Canvas(
            content=ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.PRECISE,
                on_pan_start=self.start_drawing,
                on_pan_update=self.is_drawing,
                on_pan_end=lambda e: self.save_canvas(),
                on_tap_up=self.add_point,      # Handles so we can add points
                drag_interval=20,
            ),
            expand=True,
            on_resize=self.on_canvas_resize, resize_interval=100,
        )

        self.canvas_container: ft.Container = ft.Container(
            content=self.canvas,
            expand=True, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        )

        #self.information_display: Drawing_Information_Display = Drawing_Information_Display()
        #self.mini_widgets.append(self.information_display)

        # Add notes to drawings??
        self.interactive_viewer: ft.InteractiveViewer = ft.InteractiveViewer(
            content=self.canvas_container,
        )

        self.current_path: cv.Path = cv.Path(elements=[], paint=ft.Paint(**self.story.data.get('paint_settings', {})))
       
        # Load our drawing/display
        self.load_canvas()
        self.reload_widget()

    


    # Called on launch to load our drawing from data into our canvas
    def load_canvas(self):
        """Loads our drawing from our saved map drawing file."""

        shapes = self.data.get('canvas', {})

        '''
        #OLD - Used Lines but was much more performance heavy
        
        for line in shapes.get('paths', []):
            x1, y1, x2, y2, paint_settings = line
            self.canvas.shapes.append(
                cv.Line(
                    x1, y1, x2, y2,
                    ft.Paint(**paint_settings),
                )
            )
        '''

        # Loading points
        for point in shapes.get('points', []):
            px, py, point_mode, paint_settings = point
            self.canvas.shapes.append(
                cv.Points(
                    points=[(px, py)],
                    point_mode=point_mode,
                    paint=ft.Paint(**paint_settings),
                )
            )

        

        for path in shapes.get('paths', []):
            
            elements = path.get('elements', []) # List of the elements in this path
            paint_settings = path.get('paint', {})  # Paint settings for this path

            new_path = cv.Path(elements=[], paint=ft.Paint(**paint_settings))   # Set a new path for this path with our paint settings

            # Iterate through each element for its type, and create a new path element based on that
            for element in elements:
                # MoveTo just has x and y
                if element['type'] == 'moveto':
                    new_path.elements.append(cv.Path.MoveTo(element['x'], element['y']))
                # Lineto jjust has x and y
                elif element['type'] == 'lineto':
                    new_path.elements.append(cv.Path.LineTo(element['x'], element['y']))
                else:
                    print("Unknown path element type while loading: ", element)

            self.canvas.shapes.append(new_path)
    
        

    # Called when we click the canvas and don't initiate a drag
    async def add_point(self, e: ft.TapEvent):
        ''' Adds a point to the canvas if we just clicked and didn't initiate a drag '''

        # Create the point using our paint settings and point mode
        point = cv.Points(
            points=[(e.local_x, e.local_y)],
            point_mode=self.story.data.get('canvas_settings', {}).get('point_mode', 'points'),
            paint=ft.Paint(**self.story.data.get('paint_settings', {})),
        )

        # Add point to the canvas and our state data
        self.canvas.shapes.append(point)
        self.state.points.append((e.local_x, e.local_y, point.point_mode, point.paint.__dict__))

        # After dragging canvas widget, it loses page reference and can't update
        try:
            self.canvas.update()
        except Exception as ex:
            self.p.update()
            
        # Save our canvas data
        self.save_canvas()
        
    # Called when we start drawing on the canvas
    async def start_drawing(self, e: ft.DragStartEvent):
        ''' Set our initial starting x and y coordinates for the line we're drawing '''

        # Update state x and y coordinates
        self.state.x, self.state.y = e.local_x, e.local_y

        # Clear and set our current path and state to match it
        self.current_path = cv.Path(elements=[], paint=ft.Paint(**self.story.data.get('paint_settings', {})))
        self.state.paths.clear()
        self.state.paths.append({'elements': list(), 'paint': self.story.data.get('paint_settings')})
        #self.state.paths['paint'] = self.story.data.get('paint_settings')


        # Add check for what kind of path (if one at at all) here
        

        # Set move to element at our starting position that the mouse is at for the path to start from
        move_to_element = cv.Path.MoveTo(e.local_x, e.local_y)

        # Add that element to current paths elements and our state paths
        self.current_path.elements.append(move_to_element)
        self.state.paths[0]['elements'].append((move_to_element.__dict__))
    
        # Add the path to the canvas so we can see it
        self.canvas.shapes.append(self.current_path)

        #print("Paint style: ", ft.Paint(**self.story.data.get('paint_settings', {})))

        

    # Called when actively drawing on the canvas
    async def is_drawing(self, e: ft.DragUpdateEvent):
        ''' Creates our line to add to the canvas as we draw, and saves that paths data to self.state '''

        # Sampling to improve perforamance. If the line length is too small, we skip it
        dx = e.local_x - self.state.x
        dy = e.local_y - self.state.y
        if dx * dx + dy * dy < self.min_segment_dist * self.min_segment_dist:
            return
        
        '''
        OLD - Used Lines but was much more performance heavy
        # Create our line using our previous x and y, the current x and y, and our brush settings.
        line = cv.Line(
            self.state.x, self.state.y, e.local_x, e.local_y,
            paint=ft.Paint(**self.story.data.get('paint_settings', {})),
        )

        # Store the shape so we can save it to data
        #self.state.lines.append((self.state.x, self.state.y, e.local_x, e.local_y, line.paint.__dict__))

        # Add the line to our canvas so we can see it
        self.canvas.shapes.append(line)
        '''

        # Check for what type of path we're adding here

        # Set the path element based on what kind of path we're adding, add it to our current path and our state paths
        path_element = cv.Path.LineTo(e.local_x, e.local_y)

        # Add the declared element to our current path and state paths
        self.current_path.elements.append(path_element)
        self.state.paths[0]['elements'].append((path_element.__dict__))  

        # After dragging canvas widget, it loses page reference and can't update
        try:
            self.canvas.update()
        except Exception as ex:
            self.p.update()
            #print("Canvas update failed during drawing. Updating page instead")
        

        # Update our state x and y for the next segment
        self.state.x, self.state.y = e.local_x, e.local_y
        

    # Called when we release the mouse to stop drawing a line
    def save_canvas(self):
        """ Saves our paths to our canvas data for storage """

        
        # Add on to what we already have
        if self.state.paths:
            self.data['canvas']['paths'].extend(self.state.paths)
        if self.state.points:
            self.data['canvas']['points'].extend(self.state.points)

        self.save_dict()

        # Clear the current state, otherwise it constantly grows and lags the program
        self.state.paths.clear()
        self.state.points.clear()


    

    # Called when the canvas control is resized
    async def on_canvas_resize(self, e: ft.ControlEvent):
        """Rescales stored drawing coordinates to match the new canvas size."""
        pass

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):       
        ''' Rebuilds/reloads our map UI '''

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        self.body_container.content = self.interactive_viewer

        self._render_widget()

