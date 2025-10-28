import flet as ft

# The expansion tile for the timelines and arcs on the timelines rail
class Tree_View_Expansion_Tile(ft.ExpansionTile):
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


# Class for items within a tree view on the rail
class Tree_View_Item(ft.GestureDetector):

    def __init__(
        self, 
        title: str,         # Title of this item
        on_exit,
        spacing: int = None,       # Spacing around the item. This increments. NEEDED???   
    ):
        
        self.title = title

        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.PRIMARY,
        )

        super().__init__(
            on_enter=self.handle_enter,
            on_exit=on_exit,
            content = ft.Text(value=title, style=self.text_style),
        )

    # Called when hovering mouse over a tree view item
    def handle_enter(self, e):
        print("Hovered over item: " + self.title)
