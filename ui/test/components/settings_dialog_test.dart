import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ui/components/settings_dialog.dart';
import 'package:ui/app_state.dart';

void main() {
  testWidgets('SettingsDialog displays current IP and Port',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setIp('192.168.1.1');
    appState.setPort(8080);

    await tester.pumpWidget(
      ChangeNotifierProvider<AppState>.value(
        value: appState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    expect(find.text('Settings'), findsOneWidget);
    expect(find.text('192.168.1.1'), findsOneWidget);
    expect(find.text('8080'), findsOneWidget);
  });

  testWidgets('SettingsDialog updates IP and Port',
      (WidgetTester tester) async {
    final appState = AppState();

    await tester.pumpWidget(
      ChangeNotifierProvider<AppState>.value(
        value: appState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    await tester.enterText(find.byType(TextField).at(0), '192.168.1.2');
    await tester.enterText(find.byType(TextField).at(1), '9090');

    expect(appState.ip, '192.168.1.2');
    expect(appState.port, 9090);
  });

  // testWidgets('SettingsButton opens SettingsDialog',
  //     (WidgetTester tester) async {
  //   final appState = AppState();
  //   await tester.pumpWidget(
  //     ChangeNotifierProvider<AppState>.value(
  //       value: appState,
  //       child: const MaterialApp(
  //         home: HomePage(title: 'Home Page'),
  //       ),
  //     ),
  //   );

  //   await tester.tap(find.byType(SettingsButton));
  //   await tester.pumpAndSettle();

  //   expect(find.byType(SettingsDialog), findsOneWidget);
  // });
}
