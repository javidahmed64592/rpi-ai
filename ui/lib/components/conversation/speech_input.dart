// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/audio/microphone_button.dart';
import 'package:ui/components/audio/microphone_permission_button.dart';
import 'package:ui/state/speech_state.dart';

class SpeechInput extends StatelessWidget {
  final VoidCallback onRequestPermissions;
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;

  const SpeechInput({
    Key? key,
    required this.onRequestPermissions,
    required this.onStartRecording,
    required this.onStopRecording,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<SpeechState>(
      builder: (context, speechState, child) {
        return speechState.microphonePermissionGranted
            ? MicrophoneButton(
                onStartRecording: onStartRecording,
                onStopRecording: onStopRecording,
              )
            : MicrophonePermissionButton(
                onRequestPermissions: onRequestPermissions,
              );
      },
    );
  }
}
