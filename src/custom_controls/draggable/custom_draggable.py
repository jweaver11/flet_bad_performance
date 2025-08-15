# Custom widgets needProject Structure Explanation
'''
This is a Flet user extension project that creates a custom control called FletSpinkit. Here's how the project is structured:

1. Python Package Structure (flet_spinkit)
__init__.py: Exports the main FletSpinkit class for easy importing
flet_spinkit.py: Contains the Python implementation of the custom control that extends ConstrainedControl

2. Flutter/Dart Implementation (flet_spinkit)
flet_spinkit.dart: Main library file that exports the control creation functions
create_control.dart: Factory function that creates the Flutter widget based on control type
flet_spinkit.dart: The actual Flutter widget implementation that renders the control

3. Example Application (flet_spinkit_example)
Demonstrates how to use the custom control in a Flet app
Shows the import pattern and basic usage

4. Configuration Files
pyproject.toml: Python package configuration with dependencies and build settings
pubspec.yaml: Flutter package configuration (in the Flutter directory)
How the Extension Works
Python Side: The FletSpinkit class extends Flet's ConstrainedControl and defines properties like value
Flutter Side: The FletSpinkitControl widget receives control data and renders it as a Flutter Text widget
Bridge: The createControl factory function connects the Python control name ("flet_spinkit") to the Flutter widget
How to Import Custom Controls to an Existing Project

Method 1: Install as a Dependency (Recommended)
Add to your project's pyproject.toml:
dependencies = [
    "flet-spinkit @ git+https://github.com/YourAccount/flet-spinkit",
    "flet>=0.28.3",
]

Install the package:
pip install -e .

Use in your Flet app:
import flet as ft
from flet_spinkit import FletSpinkit

def main(page: ft.Page):
    page.add(
        FletSpinkit(value="Hello from custom control!")
    )

ft.app(main)



Method 2: Local Development
Copy the extension files to your project
Install in development mode:
Build your app with the custom control:
Key Points for Using Custom Controls
Dependencies: The custom control must be installed as a dependency in your project
Building: When building your app, Flet will automatically include the Flutter implementation
Import: Import the control class from the package name (e.g., from flet_spinkit import FletSpinkit)
Versioning: Make sure your Flet version is compatible with the extension's requirements
The beauty of this structure is that it provides a seamless way to extend Flet with custom Flutter widgets while maintaining the familiar Python API for developers.

'''