import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ui/pages/home_page.dart';
import 'package:ui/app_state.dart';
import 'package:ui/components/settings_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  Widget createHomePage() {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: const MaterialApp(
        home: HomePage(),
      ),
    );
  }

  testWidgets('HomePage displays AppBar', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(AppBar), findsOneWidget);
  });

  testWidgets('HomePage displays title', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.text('Gemini'), findsOneWidget);
  });

  testWidgets('HomePage displays SettingsButton', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(SettingsButton), findsOneWidget);
  });
}
