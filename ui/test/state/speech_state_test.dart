// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/speech_state.dart';

void main() {
  group('SpeechState', () {
    late SpeechState speechState;

    setUp(() {
      speechState = SpeechState();
    });

    test('initial values are correct', () {
      expect(speechState.microphonePermissionGranted, false);
      expect(speechState.isRecording, false);
    });

    test('setMicrophonePermissionGranted', () {
      speechState.setMicrophonePermissionGranted(true);
      expect(speechState.microphonePermissionGranted, true);
    });

    test('setIsRecording', () {
      speechState.setIsRecording(true);
      expect(speechState.isRecording, true);
    });
  });
}
