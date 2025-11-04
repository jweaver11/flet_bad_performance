'''
Parent rail class used by our six workspaces. Gives uniformity to our rails
'''

import flet as ft
import os
from models.story import Story


class Rail(ft.Container):

    # Constructor
    def __init__(self, page: ft.Page, story: Story, directory_path: str):
        
        # Initialize the parent Container class first
        super().__init__(
            #padding=None,
            padding=ft.Padding(10, 0, 0, 0),        # Adds padding left to match divider on the right
        )
            
        # Page and story reference
        self.p = page
        self.story = story

        # The path this rail displays. Mostly used for adding folders on the rails
        self.directory_path = directory_path

        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.ON_SURFACE,
            weight=ft.FontWeight.BOLD,
        )

        # Declaring UI elements for easier referencing. This one is for folders, since most rails use it
        self.new_category_textfield = ft.TextField(  
            hint_text="Category Name",          
            data="category",                        # Data for logic routing on submit
            on_submit=self.submit_item,             # Called when enter is pressed
            on_change=self.on_new_item_change,      # Called on every key input
            on_blur=self.on_new_item_blur,          # Called when clicking off the textfield or after submitting
            autofocus=True,
            visible=False,
            text_style=self.text_style
        )

        # Calling initial rail to reload
        #self.reload_rail()

    def get_menu_options(self) -> list[ft.Control]:
        ''' Returns a list of menu options when right clicking child rail '''
        return []
    
    def get_sub_menu_options(self) -> list[ft.Control]:
        ''' Returns a list of additional menu options for sub-items in tree view directories '''
        return []
        

    # Called whenever our user inputs a new key into one of our textfields for new items
    def on_new_item_change(self, e):
        ''' Checks if our title is unique within its directory (default in this case) '''

        # Start out assuming we are unique
        self.item_is_unique = True

        # Grab out title from the textfield, and set our new key to compare
        title = e.control.value

        # Generate our new key to compare. Requires normalization
        nk = self.directory_path + "\\" + title
        new_key = os.path.normcase(os.path.normpath(nk))

        
        # Check all our folders and compare them to the new key
        for key in self.story.data['folders'].keys():
            
            # Path comparisons require normalization
            if os.path.normcase(os.path.normpath(key)) == new_key:
                self.item_is_unique = False
                
        # Check our chapters
        for key in self.story.chapters.keys():
            
            if os.path.normcase(os.path.normpath(key)) == new_key:
                self.item_is_unique = False

        # Check our notes
        for key in self.story.notes.keys():
            
            if os.path.normcase(os.path.normpath(key)) == new_key:
                self.item_is_unique = False
                
        # If we are NOT unique, show our error text
        if not self.item_is_unique:
            e.control.error_text = "Title must be unique"

        # Otherwise remove our error text
        else:
            e.control.error_text = None
            
        self.p.update()


    # Called when clicking off the textfield and after submission
    def on_new_item_blur(self, e):

        # Check if we're submitting, or normal blur
        if self.are_submitting:

            # Change submitting to false
            self.are_submitting = False     

            # If our item is unique, hide the textfield and update
            if self.item_is_unique:
                e.control.visible = False
                e.control.value = None
                e.control.error_text = None
                self.p.update()
                return
            
            # Otherwise its not unique, re-focus our textfield
            else:
                e.control.visible = True
                e.control.focus()
        
        # If we're not submitting, just hide the textfield and reset values
        else:
            e.control.visible = False
            e.control.value = None
            e.control.error_text = None
            self.p.update()


    # Called whenever we submit a new item (Chapter, note, category, etc.) via enter key
    def submit_item(self, e):
        ''' Sets our state to submitting, and creates new item if unique '''

        # Change our submitting state
        self.are_submitting = True

        # Grab our title from the textfield
        title = e.control.value
            
        # If our new title unique (check from on_new_item_change), create the new item
        if self.item_is_unique:

            # Check what kind of item we're creating based on textfield data
            tag = e.control.data

            # New categories
            if tag == "category":
                # Create our new category
                self.story.create_folder(
                    directory_path=self.directory_path, 
                    name=title
                )
                # This one requires reloading the rail, but the rest don't
                self.reload_rail()

            # New chapters
            elif tag == "chapter":
                self.story.create_chapter(title)

            # New Notes
            elif tag == "note":
                self.story.create_note(title)

    # Called when changes occure that require rail to be reloaded. Should be overwritten by children
    def reload_rail(self) -> ft.Control:
        ''' Sets our rail (extended ft.Container) content and applies the page update '''

        # Set your content for the rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("Base Rail - No specific content"),
                # Add more controls here as needed
            ]
        )

        # Apply the update to UI
        self.p.update()

        # Return yourself as the control
        return self