// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/state/app_state.dart';
import 'package:ui/state/speech_state.dart';

class MicrophoneButton extends StatelessWidget {
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;

  const MicrophoneButton({
    Key? key,
    required this.onStartRecording,
    required this.onStopRecording,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final speechState = Provider.of<SpeechState>(context);

    return GestureDetector(
      onLongPressStart: appState.isBusy ? null : (_) => onStartRecording(),
      onLongPressEnd: appState.isBusy ? null : (_) => onStopRecording(),
      child: Container(
        padding: const EdgeInsets.all(32),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: speechState.isRecording
              ? Theme.of(context).colorScheme.primary
              : appState.isBusy
                  ? Theme.of(context).colorScheme.onSurface.withOpacity(0.5)
                  : Theme.of(context).colorScheme.secondary,
        ),
        child: Icon(
          Icons.mic,
          color: appState.isBusy
              ? Theme.of(context).colorScheme.onSurface.withOpacity(0.5)
              : Theme.of(context).colorScheme.onSecondary,
          size: 100,
        ),
      ),
    );
  }
}
