// Flutter imports:
import 'package:flutter/material.dart';

class MicrophonePermissionButton extends StatelessWidget {
  final VoidCallback onRequestPermissions;

  const MicrophonePermissionButton({
    Key? key,
    required this.onRequestPermissions,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onRequestPermissions,
      child: Container(
        padding: const EdgeInsets.all(32),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Theme.of(context).colorScheme.secondary,
        ),
        child: Icon(
          Icons.mic_off,
          color: Theme.of(context).colorScheme.onSecondary,
          size: 100,
        ),
      ),
    );
  }
}
