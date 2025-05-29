import flet as ft

tree_view_page = ft.Page


def handle_change(e: ft.ControlEvent):
    print(f"change on panel with index {e.data}")

def handle_delete(e: ft.ControlEvent):
    panel.controls.remove(e.control.data)
    tree_view_page.page.update()

# Expansion Panels
exp1 = ft.ExpansionPanel(
    header=ft.ListTile(title=ft.Text(f"Expansion Panel 1")),
    content = ft.ListTile(
        title=ft.Text(f"This is in ExpansionPanel 1"),
        subtitle=ft.Text(f"Press the icon to hide the panel 1"),
        trailing=ft.IconButton(ft.Icons.DELETE, on_click=handle_delete),
    )
)


panel = ft.ExpansionPanelList(
    expand_icon_color=ft.Colors.AMBER,
    elevation=8,
    divider_color=ft.Colors.AMBER,
    on_change=handle_change,
    controls=[
        ft.ExpansionPanel(
            # has no header and content - placeholders will be used
            bgcolor=ft.Colors.BLUE_400,
            expanded=True,
        ),
        exp1
    ],
)

