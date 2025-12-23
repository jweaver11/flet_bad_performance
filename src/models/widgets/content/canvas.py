'''
The map class for all maps inside our story
Maps are widgets that have their own drawing canvas, and info display. they can contain nested sub maps as well.
'''

#TODO: 
# ADD DUPLICATE OPTION AS WELL
# Option for transparent background/no brackground


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
#from PIL import Image, ImageDraw



class Canvas(Widget):
    def __init__(
            self, 
            title: str, 
            page: ft.Page, 
            directory_path: str, 
            story: Story, 
            data: dict = None,
            canvas_data: dict = None,
        ):
        
        
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
                
                "canvas_meta": {        # Set canvas data here
                    "width": int,
                    "height": int,
                    "aspect_ratio": float,
                    "bgcolor": str,
                    "bgimage": str,
                },     

                #"canvas": list,          # Stores our drawing data
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

        self.canvas = cv.Canvas(
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


        

        self.canvas_container = ft.Container(
            content=self.canvas, width=2000, height=1000,
            expand=True, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            margin=ft.margin.all(20), bgcolor=ft.Colors.SURFACE,
            border=ft.border.all(2, ft.Colors.OUTLINE_VARIANT),
            #aspect_ratio=1/2,
            # Sets bgcolor or image based on canvas settings, and aspect ratio
        )


        

        #self.information_display: Drawing_Information_Display = Drawing_Information_Display()
        #self.mini_widgets.append(self.information_display)

        # Add notes to drawings??


        self.interactive_viewer = ft.InteractiveViewer(content=self.canvas_container)

        self.current_path = cv.Path(elements=[], paint=ft.Paint(**self.story.data.get('paint_settings', {})))
       
        # Load our drawing/display
        self.load_canvas()

        self.reload_widget()

    


    # Called on launch to load our drawing from data into our canvas
    def load_canvas(self):
        """Loads our drawing from our saved map drawing file."""

        shapes = self.data.get('canvas', {})


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

        # Loading paths
        for path in shapes.get('paths', []):
            
            elements = path.get('elements', [])         # List of the elements in this path
            paint_settings = path.get('paint', {})      # Paint settings for this path

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
        

        # Add check for what kind of path (if one at at all) here
        

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


    # NOT TESTED ----------------------------------
    def export_canvas(self, filename: str = "canvas_export.png", desired_width: int = 1920, desired_height: int = 1080):
        """Exports the canvas as an image at desired size, computing bounds if no meta exists."""
        shapes = self.data.get('canvas', {})
        
        # Compute bounding box from all coordinates
        min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        # Check points
        for point in shapes.get('points', []):
            px, py = point[0], point[1]
            min_x = min(min_x, px)
            min_y = min(min_y, py)
            max_x = max(max_x, px)
            max_y = max(max_y, py)
        
        # Check paths
        for path in shapes.get('paths', []):
            for element in path.get('elements', []):
                if 'x' in element and 'y' in element:
                    min_x = min(min_x, element['x'])
                    min_y = min(min_y, element['y'])
                    max_x = max(max_x, element['x'])
                    max_y = max(max_y, element['y'])
        
        # If no shapes, use defaults
        if min_x == float('inf'):
            min_x, min_y, max_x, max_y = 0, 0, desired_width, desired_height
        
        # Calculate original bounds
        orig_width = max_x - min_x
        orig_height = max_y - min_y
        
        # Avoid division by zero
        if orig_width == 0:
            orig_width = 1
        if orig_height == 0:
            orig_height = 1
        
        # Scale factor to fit desired size (maintain aspect ratio or stretch as needed)
        scale_x = desired_width / orig_width
        scale_y = desired_height / orig_height
        scale = min(scale_x, scale_y)  # To fit without cropping; use max for stretching
        
        # Create image at desired size
        #img = Image.new("RGBA", (desired_width, desired_height), (255, 255, 255, 0))
        #draw = ImageDraw.Draw(img)
        
        # Render shapes, scaled and translated
        offset_x = (desired_width - orig_width * scale) / 2  # Center horizontally
        offset_y = (desired_height - orig_height * scale) / 2  # Center vertically
        
        # Render points
        for point in shapes.get('points', []):
            px, py, point_mode, paint_settings = point
            scaled_x = (px - min_x) * scale + offset_x
            scaled_y = (py - min_y) * scale + offset_y
            # Draw as circle (adapt for point_mode)
            #draw.ellipse((scaled_x-2, scaled_y-2, scaled_x+2, scaled_y+2), fill=paint_settings.get('color', 'black'))
        
        # Render paths (simplified; full path rendering needs more logic for curves)
        for path in shapes.get('paths', []):
            paint_settings = path.get('paint', {})
            points = []
            for element in path.get('elements', []):
                if element['type'] in ['moveto', 'lineto']:
                    scaled_x = (element['x'] - min_x) * scale + offset_x
                    scaled_y = (element['y'] - min_y) * scale + offset_y
                    points.append((scaled_x, scaled_y))
            #if points:
                #draw.line(points, fill=paint_settings.get('color', 'black'), width=2)
        
        #img.save(os.path.join(self.directory_path, filename))
        self.page.snack_bar = Snack_Bar(f"Canvas exported to {filename} at {desired_width}x{desired_height}")
        self.page.snack_bar.open = True
        self.page.update()

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):       
        ''' Rebuilds/reloads our map UI '''

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        self.body_container.alignment = ft.alignment.center

        self.body_container.content = self.interactive_viewer

        self._render_widget()


