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

    test('updateConfig updates all values', () {
      settingsState.updateConfig({
        'model': 'newModel',
        'systemInstruction': 'newSystemInstruction',
        'candidateCount': 2,
        'maxOutputTokens': 2000,
        'temperature': 2.0,
      });
      expect(settingsState.model, 'newModel');
      expect(settingsState.systemInstruction, 'newSystemInstruction');
      expect(settingsState.candidateCount, 2);
      expect(settingsState.maxOutputTokens, 2000);
      expect(settingsState.temperature, 2.0);
    });
  });
}
