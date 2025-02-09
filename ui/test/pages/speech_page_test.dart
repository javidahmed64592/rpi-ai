// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/audio/status_display_box.dart';
import 'package:ui/components/conversation/speech_input.dart';
import 'package:ui/pages/speech_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/speech_state.dart';

void main() {
  late AppState appState;
  late NotificationState notificationState;
  late SpeechState speechState;

  setUp(() {
    appState = AppState();
    notificationState = NotificationState();
    speechState = SpeechState();
  });

  Widget createSpeechPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => appState),
        ChangeNotifierProvider(create: (_) => notificationState),
        ChangeNotifierProvider(create: (_) => speechState),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: SpeechPage(),
        ),
      ),
    );
  }

  testWidgets('SpeechPage initializes correctly', (WidgetTester tester) async {
    await tester.pumpWidget(createSpeechPage());

    expect(find.byType(SpeechPage), findsOneWidget);
    expect(find.byType(StatusDisplayBox), findsNWidgets(2));
    expect(find.byType(SpeechInput), findsOneWidget);
  });
}
