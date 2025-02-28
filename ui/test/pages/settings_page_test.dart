// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/settings_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';
import 'package:ui/types.dart';
import 'settings_page_test.mocks.dart';

@GenerateMocks([HttpHelper])
void main() {
  late MockHttpHelper mockHttpHelper;

  setUp(() {
    mockHttpHelper = MockHttpHelper();
  });

  Widget createSettingsPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
        ChangeNotifierProvider(create: (_) => MessageState()),
        ChangeNotifierProvider(create: (_) => NotificationState()),
        ChangeNotifierProvider(create: (_) => SettingsState()),
      ],
      child: MaterialApp(
        home: Scaffold(
          body: SettingsPage(httpHelper: mockHttpHelper),
        ),
      ),
    );
  }

  testWidgets('SettingsPage displays all text fields',
      (WidgetTester tester) async {
    await tester.pumpWidget(createSettingsPage());

    expect(find.byType(TextField), findsNWidgets(4));
    expect(find.widgetWithText(TextField, 'Model'), findsOneWidget);
    expect(
        find.widgetWithText(TextField, 'System Instruction'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Max Output Tokens'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Temperature'), findsOneWidget);
  });

  testWidgets('SettingsPage displays all buttons', (WidgetTester tester) async {
    await tester.pumpWidget(createSettingsPage());

    expect(find.widgetWithText(ElevatedButton, 'Update'), findsOneWidget);
    expect(find.widgetWithText(ElevatedButton, 'Restart Chat'), findsOneWidget);
    expect(find.widgetWithText(ElevatedButton, 'Logout'), findsOneWidget);
  });

  testWidgets('Update button triggers config update',
      (WidgetTester tester) async {
    when(mockHttpHelper.updateConfig(any, any, any)).thenAnswer((_) async => [
          {'text': 'Config updated successfully', 'isUserMessage': false},
        ]);
    await tester.pumpWidget(createSettingsPage());

    await tester.enterText(find.byType(TextField).at(0), 'newModel');
    await tester.enterText(
        find.byType(TextField).at(1), 'newSystemInstruction');
    await tester.enterText(find.byType(TextField).at(2), '1500');
    await tester.enterText(find.byType(TextField).at(3), '1.5');

    await tester.tap(find.text('Update'));
    await tester.pumpAndSettle();

    final settingsState = Provider.of<SettingsState>(
        tester.element(find.byType(MaterialApp)),
        listen: false);
    final messageState = Provider.of<MessageState>(
        tester.element(find.byType(MaterialApp)),
        listen: false);
    expect(settingsState.model, 'newModel');
    expect(settingsState.systemInstruction, 'newSystemInstruction');
    expect(settingsState.maxOutputTokens, 1500);
    expect(settingsState.temperature, 1.5);
    expect(messageState.messages.length, 1);
    expect(
      messageState.messages[0],
      {'text': 'Config updated successfully', 'isUserMessage': false},
    );
  });

  testWidgets('Restart Chat button triggers chat restart',
      (WidgetTester tester) async {
    when(mockHttpHelper.postRestartChat(any, any)).thenAnswer((_) async => [
          {'text': 'Chat restarted', 'is_user_message': false},
          {'text': 'Welcome back', 'is_user_message': true}
        ]);

    await tester.pumpWidget(createSettingsPage());

    final restartChatButton =
        find.widgetWithText(ElevatedButton, 'Restart Chat');
    await tester.tap(restartChatButton);
    await tester.pumpAndSettle();

    final messageState = Provider.of<MessageState>(
        tester.element(find.byType(SettingsPage)),
        listen: false);
    expect(messageState.messages.length, 2);
    expect(messageState.messages[0],
        {'text': 'Chat restarted', 'is_user_message': false});
    expect(messageState.messages[1],
        {'text': 'Welcome back', 'is_user_message': true});
  });

  testWidgets('Logout button triggers logout process',
      (WidgetTester tester) async {
    await tester.pumpWidget(createSettingsPage());

    final logoutButton = find.widgetWithText(ElevatedButton, 'Logout');
    await tester.tap(logoutButton);
    await tester.pumpAndSettle();

    final appState = Provider.of<AppState>(
        tester.element(find.byType(SettingsPage)),
        listen: false);
    expect(appState.connected, false);
  });

  testWidgets('Displays error message on failed config update',
      (WidgetTester tester) async {
    when(mockHttpHelper.updateConfig(any, any, any))
        .thenThrow(Exception('Failed to update config'));

    await tester.pumpWidget(createSettingsPage());

    final updateButton = find.widgetWithText(ElevatedButton, 'Update');
    await tester.tap(updateButton);
    await tester.pumpAndSettle();

    final notificationState = Provider.of<NotificationState>(
        tester.element(find.byType(SettingsPage)),
        listen: false);
    expect(notificationState.notificationState, NotificationType.error);
    expect(notificationState.notificationMessage,
        'Error updating settings: Exception: Failed to update config');
  });

  testWidgets('Displays error message on failed chat restart',
      (WidgetTester tester) async {
    when(mockHttpHelper.postRestartChat(any, any))
        .thenThrow(Exception('Failed to restart chat'));

    await tester.pumpWidget(createSettingsPage());

    final restartChatButton =
        find.widgetWithText(ElevatedButton, 'Restart Chat');
    await tester.tap(restartChatButton);
    await tester.pumpAndSettle();

    final notificationState = Provider.of<NotificationState>(
        tester.element(find.byType(SettingsPage)),
        listen: false);
    expect(notificationState.notificationState, NotificationType.error);
    expect(notificationState.notificationMessage,
        'Error restarting chat: Exception: Failed to restart chat');
  });
}
