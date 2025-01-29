// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/settings_state.dart';

void main() {
  group('SettingsState', () {
    late SettingsState settingsState;

    setUp(() {
      settingsState = SettingsState();
    });

    test('initial values are correct', () {
      expect(settingsState.model, '');
      expect(settingsState.systemInstruction, '');
      expect(settingsState.candidateCount, 1);
      expect(settingsState.maxOutputTokens, 1000);
      expect(settingsState.temperature, 1.0);
    });

    test('setModel updates model', () {
      settingsState.setModel('newModel');
      expect(settingsState.model, 'newModel');
    });

    test('setSystemInstruction updates systemInstruction', () {
      settingsState.setSystemInstruction('newSystemInstruction');
      expect(settingsState.systemInstruction, 'newSystemInstruction');
    });

    test('setCandidateCount updates candidateCount', () {
      settingsState.setCandidateCount(2);
      expect(settingsState.candidateCount, 2);
    });

    test('setMaxOutputTokens updates maxOutputTokens', () {
      settingsState.setMaxOutputTokens(2000);
      expect(settingsState.maxOutputTokens, 2000);
    });

    test('setTemperature updates temperature', () {
      settingsState.setTemperature(2.0);
      expect(settingsState.temperature, 2.0);
    });
  });
}
