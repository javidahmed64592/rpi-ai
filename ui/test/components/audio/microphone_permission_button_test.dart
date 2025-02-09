// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/audio/microphone_permission_button.dart';

void main() {
  Widget createMicrophonePermissionButton(VoidCallback onRequestPermissions) {
    return MaterialApp(
      home: Scaffold(
        body: MicrophonePermissionButton(
          onRequestPermissions: onRequestPermissions,
        ),
      ),
    );
  }

  testWidgets(
      'MicrophonePermissionButton triggers onRequestPermissions callback',
      (WidgetTester tester) async {
    bool callbackTriggered = false;

    void onRequestPermissions() {
      callbackTriggered = true;
    }

    await tester.pumpWidget(
      createMicrophonePermissionButton(onRequestPermissions),
    );

    await tester.tap(find.byType(GestureDetector));
    expect(callbackTriggered, isTrue);
  });

  testWidgets('MicrophonePermissionButton displays mic_off icon',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      createMicrophonePermissionButton(() {}),
    );

    final iconFinder = find.byIcon(Icons.mic_off);
    expect(iconFinder, findsOneWidget);
  });
}
