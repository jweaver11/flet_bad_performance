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
PSEUDO CODE/EXPLANATION 4 ME:
Draggable<Border>(
    data: how should look
    child: what shows when not dragging
    feedback: what shows when dragging
    childWhenDragging: what shows in place of child when dragging
    onDragStarted: what to do when drag starts
    onDragEnd: what to do when drag ends
    onDraggableCanceled: what to do when drag is canceled
    onDragCompleted: what to do when drag completes)
'''