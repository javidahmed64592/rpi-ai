// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/audio/microphone_button.dart';
import 'package:ui/state/speech_state.dart';

void main() {
  late SpeechState speechState;

  setUp(() {
    speechState = SpeechState();
  });

  Widget createMicrophoneButton(
      VoidCallback onStartRecording, VoidCallback onStopRecording) {
    return ChangeNotifierProvider<SpeechState>.value(
      value: speechState,
      child: MaterialApp(
        home: Scaffold(
          body: MicrophoneButton(
            onStartRecording: onStartRecording,
            onStopRecording: onStopRecording,
          ),
        ),
      ),
    );
  }

  testWidgets('MicrophoneButton displays correctly when not recording or busy',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMicrophoneButton(() {}, () {}));

    final iconFinder = find.byIcon(Icons.mic);
    expect(iconFinder, findsOneWidget);
  });
  testWidgets('MicrophoneButton displays correctly when recording',
      (WidgetTester tester) async {
    speechState.setIsRecording(true);
    await tester.pumpWidget(createMicrophoneButton(() {}, () {}));

    final iconFinder = find.byIcon(Icons.mic);
    expect(iconFinder, findsOneWidget);
  });

  testWidgets('MicrophoneButton starts and stops recording when not busy',
      (WidgetTester tester) async {
    bool startRecordingCalled = false;
    bool stopRecordingCalled = false;

    void onStartRecording() {
      startRecordingCalled = true;
    }

    void onStopRecording() {
      stopRecordingCalled = true;
    }

    await tester
        .pumpWidget(createMicrophoneButton(onStartRecording, onStopRecording));

    final iconFinder = find.byIcon(Icons.mic);
    expect(iconFinder, findsOneWidget);

    await tester.longPress(find.byType(GestureDetector));
    expect(startRecordingCalled, isTrue);
    expect(stopRecordingCalled, isTrue);
  });

  testWidgets('MicrophoneButton does not start recording when busy',
      (WidgetTester tester) async {
    bool startRecordingCalled = false;
    bool stopRecordingCalled = false;

    void onStartRecording() {
      startRecordingCalled = true;
    }

    void onStopRecording() {
      stopRecordingCalled = true;
    }

    speechState.setIsBusy(true);
    await tester
        .pumpWidget(createMicrophoneButton(onStartRecording, onStopRecording));

    final iconFinder = find.byIcon(Icons.mic);
    expect(iconFinder, findsOneWidget);

    await tester.longPress(find.byType(GestureDetector));
    expect(startRecordingCalled, isFalse);
    expect(stopRecordingCalled, isFalse);
  });
}
