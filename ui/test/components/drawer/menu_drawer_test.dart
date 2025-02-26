// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/drawer/menu_drawer.dart';
import 'package:ui/components/drawer/menu_item.dart';
import 'package:ui/state/app_state.dart';

void main() {
  Widget createMenuDrawer() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: MenuDrawer(),
        ),
      ),
    );
  }

  testWidgets('MenuDrawer has 3 menu items', (WidgetTester tester) async {
    await tester.pumpWidget(createMenuDrawer());

    expect(find.byType(Drawer), findsOneWidget);
    expect(find.byType(ListView), findsOneWidget);
    expect(find.byType(DrawerHeader), findsOneWidget);
    expect(find.text('Switch page'), findsOneWidget);
    expect(find.byType(MenuItem), findsNWidgets(3));
  });

  testWidgets('MenuDrawer menu items have correct titles',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMenuDrawer());

    expect(find.text('Chat'), findsOneWidget);
    expect(find.text('Speech'), findsOneWidget);
    expect(find.text('Settings'), findsOneWidget);
  });
}
