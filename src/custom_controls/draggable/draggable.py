'''WIP'''
#reference: https://api.flutter.dev/flutter/widgets/Draggable-class.html
'''
import 'package:flutter/material.dart';

TODO: check/redo names here
class DraggableWidget extends StatelessWidget {
    const DraggableWidget({super.key});
    
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            home: Scaffold(
                appBar: AppBar(title: const Text('DRAG ME!')),
                body: const DraggableExample(),
            ),
        );
    }
}

TODO: add classes for "draggableExample" and "draggableExampleState"


'''