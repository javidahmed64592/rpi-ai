// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  Widget createCustomAppBar() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: CustomAppBar(),
        ),
      ),
    );
  }

  testWidgets('CustomAppBar displays title for login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setPageLogin();
    await tester.pump();
    expect(find.text(PageType.login.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for text page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setPageText();
    await tester.pump();
    expect(find.text(PageType.text.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for speech page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setPageSpeech();
    await tester.pump();
    expect(find.text(PageType.speech.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for settings page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setPageSettings();
    await tester.pump();
    expect(find.text(PageType.settings.title), findsOneWidget);
  });
}
