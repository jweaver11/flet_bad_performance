'''
The map class for all maps inside our story
Maps are widgets that have their own drawing canvas, and info display. they can contain nested sub maps as well.
'''

#TODO: 
# ADD DUPLICATE OPTION AS WELL
# Option for transparent background/no brackground
# Option to upload image as background
# Option to export canvas as image file (png, jpg, etc). Option to change how image fits on canvas (stretch, fit, fill, tile, center, etc)
# Add ft.DecorationImage options to the canvas container for background images
# Add color_filter for both decoration image and container ?
# Fill tool??


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
        bgcolor: str = None,
        bgimage_path: str = None,
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
                    "bgcolor": bgcolor,
                    "bgimage_path": bgimage_path,
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
            margin=ft.margin.all(20), bgcolor=ft.Colors.SURFACE if bgcolor is None else bgcolor,
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

            # Grab our style for simple logic
            style = path.get('paint', {}).get('style', 'stroke')

            # Make a copy of our paint settings to modify for drawing
            safe_paint_settings = path.get('paint', {}).copy()

            # Set stroke or fill based on custom styles
            safe_stroke = 'fill' if style.endswith('fill') else 'stroke'
            safe_paint_settings['style'] = safe_stroke

            new_path = cv.Path(elements=[], paint=ft.Paint(**safe_paint_settings))   # Set a new path for this path with our paint settings

            # Iterate through each element for its type, and create a new path element based on that
            for element in elements:

                # MoveTo just has x and y
                if element['type'] == 'moveto':
                    new_path.elements.append(cv.Path.MoveTo(element['x'], element['y']))

                # Lineto jjust has x and y
                elif element['type'] == 'lineto':
                    new_path.elements.append(cv.Path.LineTo(element['x'], element['y']))

                # QuadraticTo has cp1x, cp1y, x, y, w
                elif element['type'] == 'arcto':
                    new_path.elements.append(
                        cv.Path.ArcTo(
                            radius=element['radius'],
                            rotation=element['rotation'],
                            large_arc=element['large_arc'],
                            x=element['x'],
                            y=element['y'],
                        )
                    )

                
                else:
                    print("Unknown path element type while loading: ", element)
                    self.p.open(Snack_Bar(f"Error loading {self.title}"))

            self.canvas.shapes.append(new_path)
 

         

    # Called when we click the canvas and don't initiate a drag
    async def add_point(self, e: ft.TapEvent):
        ''' Adds a point to the canvas if we just clicked and didn't initiate a drag '''

         # Create the point using our paint settings and point mode
        point = cv.Points(
            points=[(e.local_x, e.local_y)],
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

        # Grab our style so we can compare it
        style = str(self.story.data.get('paint_settings', {}).get('style', 'stroke'))

        # Make a copy of our paint settings to modify it, since some of the styles are not built in
        safe_paint_settings = self.story.data.get('paint_settings', {}).copy()

        # Set either stroke or fill based on custom styles
        safe_stroke = 'fill' if style.endswith('fill') else 'stroke'
        safe_paint_settings['style'] = safe_stroke

        print(safe_paint_settings)

        # Update state x and y coordinates
        self.state.x, self.state.y = e.local_x, e.local_y

        # Clear and set our current path and state to match it
        self.current_path = cv.Path(elements=[], paint=ft.Paint(**safe_paint_settings))
        self.state.paths.clear()
        self.state.paths.append({'elements': list(), 'paint': self.story.data.get('paint_settings')})

        # Set move to element at our starting position that the mouse is at for the path to start from
        move_to_element = cv.Path.MoveTo(e.local_x, e.local_y)

        # Add that element to current paths elements and our state paths
        self.current_path.elements.append(move_to_element)
        self.state.paths[0]['elements'].append((move_to_element.__dict__))

        print(f"Starting drawing with style {style}")

        # If we're using lineto (straight lines), add that element to the current path and state right away
        if style == "lineto":
            line_element = cv.Path.LineTo(e.local_x, e.local_y)
            self.current_path.elements.append(line_element)
            self.state.paths[0]['elements'].append((line_element.__dict__))

        # Else if we're using arcto, add that element to the current path and state right away
        elif style == 'arcto' or style == 'arctofill':
            arc_element = cv.Path.ArcTo(
                radius=12,
                rotation=0,
                large_arc=False,
                x=e.local_x,
                y=e.local_y,
            )
            self.current_path.elements.append(arc_element)
            self.state.paths[0]['elements'].append((arc_element.__dict__))

        # Add the path to the canvas so we can see it
        self.canvas.shapes.append(self.current_path)


        
    # Called when actively drawing on the canvas
    async def is_drawing(self, e: ft.DragUpdateEvent):
        ''' Creates our line to add to the canvas as we draw, and saves that paths data to self.state '''

        # Sampling to improve perforamance. If the line length is too small, we skip it
        dx = e.local_x - self.state.x
        dy = e.local_y - self.state.y
        if dx * dx + dy * dy < self.min_segment_dist * self.min_segment_dist:
            return
        
        # Grab our style so we can compare it
        style = str(self.story.data.get('paint_settings', {}).get('style', 'stroke'))


        # Handle lineto (Straight lines). Grab the element we created on start drawing, update its data
        if style == "lineto":
            
            # Set the element and its data
            line_element = self.current_path.elements[-1]
            line_dict = line_element.__dict__

            # Update the elements position
            line_element.x = e.local_x
            line_element.y = e.local_y

            # Update the dict to match
            line_dict['x'] = line_element.x
            line_dict['y'] = line_element.y

            # Update the page and return early
            try:
                self.canvas.update()
            except Exception as ex:
                self.p.update()
            return
        
        # Handle arcs
        if style == 'arcto' or style == 'arctofill':
            
            arc_element = self.current_path.elements[-1]
            arc_dict = arc_element.__dict__

            arc_element.x = e.local_x
            arc_element.y = e.local_y
        

            arc_dict['x'] = arc_element.x
            arc_dict['y'] = arc_element.y

            # Update the page and return early
            try:
                self.canvas.update()
            except Exception as ex:
                self.p.update()
            return
        
        
        # If its not one of our custom styles, use free-draw stroke, which is constantly adding line_to segements
        else:

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
        self.page.open(Snack_Bar(f"Canvas exported to {filename} at {desired_width}x{desired_height}"))
        self.page.update()

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):       
        ''' Rebuilds/reloads our map UI '''

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        self.canvas_container.content = self.canvas

        self.canvas_container.image = ft.DecorationImage(self.data.get('canvas_meta', {}).get('bgimage_path', ""), fit=ft.ImageFit.COVER) if self.data['canvas_meta'].get('bgimage_path', "") != "" else None

        self.body_container.alignment = ft.alignment.center


        self.body_container.content = self.interactive_viewer

        self._render_widget()


