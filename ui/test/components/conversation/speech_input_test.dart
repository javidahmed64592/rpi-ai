// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/audio/microphone_button.dart';
import 'package:ui/components/audio/microphone_permission_button.dart';
import 'package:ui/components/conversation/speech_input.dart';
import 'package:ui/state/speech_state.dart';

void main() {
  late SpeechState speechState;

  setUp(() {
    speechState = SpeechState();
  });

  Widget createSpeechInput(VoidCallback onRequestPermissions,
      VoidCallback onStartRecording, VoidCallback onStopRecording) {
    return ChangeNotifierProvider<SpeechState>.value(
      value: speechState,
      child: MaterialApp(
        home: Scaffold(
          body: SpeechInput(
            onRequestPermissions: onRequestPermissions,
            onStartRecording: onStartRecording,
            onStopRecording: onStopRecording,
          ),
        ),
      ),
    );
  }

  testWidgets(
      'SpeechInput displays correctly when microphone permission granted',
      (WidgetTester tester) async {
    speechState.setMicrophonePermissionGranted(true);
    await tester.pumpWidget(createSpeechInput(() {}, () {}, () {}));

    final microphoneButtonFinder = find.byType(MicrophoneButton);
    expect(microphoneButtonFinder, findsOneWidget);
  });

  testWidgets(
      'SpeechInput displays correctly when microphone permission not granted',
      (WidgetTester tester) async {
    speechState.setMicrophonePermissionGranted(false);
    await tester.pumpWidget(createSpeechInput(() {}, () {}, () {}));

    final microphonePermissionButtonFinder =
        find.byType(MicrophonePermissionButton);
    expect(microphonePermissionButtonFinder, findsOneWidget);
  });
}
