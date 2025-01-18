// Flutter imports:
import 'package:flutter/material.dart';

class TimeoutDialog extends StatefulWidget {
  final VoidCallback retryConnection;

  const TimeoutDialog({Key? key, required this.retryConnection})
      : super(key: key);

  @override
  State<TimeoutDialog> createState() => _TimeoutDialogState();
}

class _TimeoutDialogState extends State<TimeoutDialog> {
  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Connection Lost'),
      content: const Text('The connection has been lost. Please try again.'),
      actions: <Widget>[
        Center(
          child: ElevatedButton(
            onPressed: () {
              widget.retryConnection();
            },
            child: const Text('Retry Connection'),
          ),
        ),
      ],
    );
  }
}
