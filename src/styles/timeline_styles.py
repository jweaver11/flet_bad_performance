'''
Extended flet controls that implement the same styling for easy access
'''

import flet as ft

# The expansion tile for the timelines and arcs on the timelines rail
class Timeline_Expansion_Tile(ft.ExpansionTile):
    def __init__(self, title, controls=None, on_change=None, scale=None):
        super().__init__(
            title=ft.Text(title),
            text_color="primary",
            #dense=True,
            #expanded_alignment=ft.Alignment(-.5, -.5),
            expanded_alignment=ft.alignment.center_right,
            #expanded_cross_axis_alignment=ft.CrossAxisAlignment.CENTER,
            #padding=ft.Padding(left=10, top=0, right=0, bottom=0),
            #bgcolor=ft.Colors.GREY_200,
            maintain_state=True,
            #icon_color=ft.Colors.BLUE_900,
            shape=ft.RoundedRectangleBorder(),
            #controls=controls if controls else [],
            controls=[ft.Container(height=6)],
            #on_change=on_change,
            scale=scale if scale is not None else 1.0
        )


# The controls for timelines inside the timeline widget
class Timeline_Item(ft.GestureDetector):
    def __init__(self, on_enter, on_exit, axis):

        # Set our content based on axis
        self.axis = axis

        super().__init__(
            on_enter=on_enter,
            on_exit=on_exit,
            #content=ft.VerticalDivider(color=ft.Colors.with_opacity(0.7, ft.Colors.BLUE), thickness=4),
        )