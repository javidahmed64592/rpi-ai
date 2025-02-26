// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/drawer/menu_item.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  Widget createMenuItem(PageType page) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: MaterialApp(
        home: Scaffold(
          body: MenuItem(page: page),
        ),
      ),
    );
  }

  testWidgets('MenuItem displays text page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.text;
    await tester.pumpWidget(createMenuItem(page));
    expect(find.text(page.title), findsOneWidget);
    expect(find.byIcon(page.icon), findsOneWidget);
  });

  testWidgets('MenuItem for text page changes page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.text;
    await tester.pumpWidget(createMenuItem(page));
    await tester.tap(find.byType(MenuItem));
    final appState = Provider.of<AppState>(
        tester.element(find.byType(MenuItem)),
        listen: false);
    expect(appState.activePage, page);
  });

  testWidgets('MenuItem displays speech page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.speech;
    await tester.pumpWidget(createMenuItem(page));
    expect(find.text(page.title), findsOneWidget);
    expect(find.byIcon(page.icon), findsOneWidget);
  });

  testWidgets('MenuItem for speech page changes page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.speech;
    await tester.pumpWidget(createMenuItem(page));
    await tester.tap(find.byType(MenuItem));
    final appState = Provider.of<AppState>(
        tester.element(find.byType(MenuItem)),
        listen: false);
    expect(appState.activePage, page);
  });

  testWidgets('MenuItem displays settings page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.settings;
    await tester.pumpWidget(createMenuItem(page));
    expect(find.text(page.title), findsOneWidget);
    expect(find.byIcon(page.icon), findsOneWidget);
  });

  testWidgets('MenuItem for settings page changes page correctly',
      (WidgetTester tester) async {
    PageType page = PageType.settings;
    await tester.pumpWidget(createMenuItem(page));
    await tester.tap(find.byType(MenuItem));
    final appState = Provider.of<AppState>(
        tester.element(find.byType(MenuItem)),
        listen: false);
    expect(appState.activePage, page);
  });
}
