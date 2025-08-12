import flet as ft
import threading
import time

class DragManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_draggable = None
            cls._instance.check_timer = None
        return cls._instance
    
    def set_current_draggable(self, draggable):
        self.current_draggable = draggable
        # Start checking for drag completion
        self.start_drag_check()
    
    def mark_accepted(self):
        if self.current_draggable:
            print("DEBUG: Marking drag as accepted")
            self.current_draggable._drag_accepted = True
    
    def start_drag_check(self):
        # Cancel any existing timer
        if self.check_timer:
            self.check_timer.cancel()
        
        # Start a new timer to check drag completion
        self.check_timer = threading.Timer(0.5, self.check_drag_completion)
        self.check_timer.start()
    
    def check_drag_completion(self):
        if self.current_draggable and not self.current_draggable._drag_accepted:
            print("DEBUG: Timer expired - triggering cancel")
            if self.current_draggable._on_cancel:
                self.current_draggable._on_cancel()
        self.clear_current()
    
    def clear_current(self):
        if self.check_timer:
            self.check_timer.cancel()
            self.check_timer = None
        self.current_draggable = None

# Global instance
drag_manager = DragManager()

class MyDraggable(ft.Draggable):
    def __init__(self, on_cancel=None, **kwargs):
        super().__init__(**kwargs)
        self._on_cancel = on_cancel
        self._drag_started = False
        self._drag_accepted = False
        
        # Override the drag events
        original_on_drag_start = kwargs.get('on_drag_start')
        original_on_drag_complete = kwargs.get('on_drag_complete')
        
        self.on_drag_start = self._handle_drag_start
        self.on_drag_complete = self._handle_drag_complete
        
        # Store original handlers
        self._original_on_drag_start = original_on_drag_start
        self._original_on_drag_complete = original_on_drag_complete
    
    def _handle_drag_start(self, e):
        print("DEBUG: Drag started")
        self._drag_started = True
        self._drag_accepted = False
        drag_manager.set_current_draggable(self)
        
        if self._original_on_drag_start:
            self._original_on_drag_start(e)
    
    def _handle_drag_complete(self, e):
        print("DEBUG: Drag completed successfully")
        self._drag_started = False
        self._drag_accepted = True
        drag_manager.clear_current()
        
        if self._original_on_drag_complete:
            self._original_on_drag_complete(e)

class MyDragTarget(ft.DragTarget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        original_on_accept = kwargs.get('on_accept')
        self.on_accept = self._handle_accept
        self._original_on_accept = original_on_accept
    
    def _handle_accept(self, e):
        print("DEBUG: Drag target accepted")
        drag_manager.mark_accepted()
        
        if self._original_on_accept:
            self._original_on_accept(e)

