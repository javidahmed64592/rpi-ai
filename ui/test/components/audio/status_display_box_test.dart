// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/audio/status_display_box.dart';

void main() {
  Widget createStatusDisplayBox(bool showPrimary) {
    return MaterialApp(
      home: Scaffold(
        body: StatusDisplayBox(
          primaryMessage: 'Primary Message',
          secondaryMessage: 'Secondary Message',
          primaryIcon: Icons.check,
          secondaryIcon: Icons.close,
          primaryColor: Colors.green,
          secondaryColor: Colors.red,
          showPrimary: showPrimary,
        ),
      ),
    );
  }

  testWidgets(
      'StatusDisplayBox displays primary message and icon when showPrimary is true',
      (WidgetTester tester) async {
    await tester.pumpWidget(createStatusDisplayBox(true));

    expect(find.text('Primary Message'), findsOneWidget);
    expect(find.byIcon(Icons.check), findsOneWidget);
  });

  testWidgets(
      'StatusDisplayBox displays secondary message and icon when showPrimary is false',
      (WidgetTester tester) async {
    await tester.pumpWidget(createStatusDisplayBox(false));

    expect(find.text('Secondary Message'), findsOneWidget);
    expect(find.byIcon(Icons.close), findsOneWidget);
  });
}
