'''WIP'''
#reference: https://api.flutter.dev/flutter/widgets/Draggable-class.html
'''
import 'package:flutter/material.dart';

TODO: check/redo names here - this was built off of the example but i don't think it works here also unfinished
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
    data: how should look - the border perhaps ref to existing border?
    child: what shows when not dragging - the border ^
    feedback: what shows when dragging - same but with opacity
    childWhenDragging: what shows in place of child when dragging - empty 
    onDragStarted: what to do when drag starts - start moving the border?
    onDragEnd: what to do when drag ends - establish new position
    onDraggableCanceled: what to do when drag is canceled - return to original position
    onDragCompleted: what to do when drag completes - finalize new position
'''