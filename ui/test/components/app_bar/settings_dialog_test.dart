// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';
import 'package:ui/types.dart';
import 'settings_dialog_test.mocks.dart';

@GenerateMocks([HttpHelper])
void main() {
  late AppState appState;
  late MockHttpHelper mockHttpHelper;

  setUp(() {
    appState = AppState();
    mockHttpHelper = MockHttpHelper();
  });

  Widget createSettingsDialog() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => appState),
        ChangeNotifierProvider(create: (_) => MessageState()),
        ChangeNotifierProvider(create: (_) => NotificationState()),
        ChangeNotifierProvider(create: (_) => SettingsState()),
      ],
      child: MaterialApp(
        home: Scaffold(
          body: SettingsDialog(httpHelper: mockHttpHelper),
        ),
      ),
    );
  }

  Widget createSettingsButton() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => appState),
        ChangeNotifierProvider(create: (_) => MessageState()),
        ChangeNotifierProvider(create: (_) => NotificationState()),
        ChangeNotifierProvider(create: (_) => SettingsState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: SettingsButton(),
        ),
      ),
    );
  }

  testWidgets('SettingsButton opens SettingsDialog',
      (WidgetTester tester) async {
    await tester.pumpWidget(createSettingsButton());

    await tester.tap(find.byType(SettingsButton));
    await tester.pumpAndSettle();

    expect(find.byType(SettingsDialog), findsOneWidget);
    expect(find.text('Update'), findsOneWidget);
    expect(find.text('Close'), findsOneWidget);
  });

  testWidgets('SettingsButton does not open SettingsDialog when busy',
      (WidgetTester tester) async {
    appState.setIsBusy(true);
    await tester.pumpWidget(createSettingsButton());

    await tester.tap(find.byType(SettingsButton));
    await tester.pumpAndSettle();

    expect(find.byType(SettingsDialog), findsNothing);
  });

  testWidgets(
      'SettingsDialog updates SettingsState when Update button is pressed',
      (WidgetTester tester) async {
    when(mockHttpHelper.updateConfig(any, any, any)).thenAnswer((_) async => [
          {'text': 'Config updated successfully', 'isUserMessage': false},
        ]);

    await tester.pumpWidget(createSettingsDialog());

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.enterText(find.byType(TextField).at(0), 'newModel');
    await tester.enterText(
        find.byType(TextField).at(1), 'newSystemInstruction');
    await tester.enterText(find.byType(TextField).at(2), '5');
    await tester.enterText(find.byType(TextField).at(3), '1500');
    await tester.enterText(find.byType(TextField).at(4), '1.5');

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
    expect(settingsState.candidateCount, 5);
    expect(settingsState.maxOutputTokens, 1500);
    expect(settingsState.temperature, 1.5);
    expect(messageState.messages.length, 1);
    expect(
      messageState.messages[0],
      {'text': 'Config updated successfully', 'isUserMessage': false},
    );

    expect(find.byType(AlertDialog), findsNothing);
  });

  testWidgets(
      'SettingsDialog shows error notification when Update button is pressed and an error occurs',
      (WidgetTester tester) async {
    when(mockHttpHelper.updateConfig(any, any, any))
        .thenThrow(Exception('Failed to update config'));

    await tester.pumpWidget(createSettingsDialog());

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.tap(find.text('Update'));
    await tester.pumpAndSettle();

    final notificationState = Provider.of<NotificationState>(
        tester.element(find.byType(MaterialApp)),
        listen: false);
    expect(notificationState.notificationState, NotificationType.error);
    expect(notificationState.notificationMessage,
        'Error updating settings: Exception: Failed to update config');

    expect(find.byType(AlertDialog), findsNothing);
  });

  testWidgets(
      'SettingsDialog restarts chat when Restart Chat button is pressed',
      (WidgetTester tester) async {
    when(mockHttpHelper.postRestartChat(any, any)).thenAnswer((_) async => [
          {'text': 'Chat restarted', 'is_user_message': false},
          {'text': 'Welcome back', 'is_user_message': true}
        ]);

    await tester.pumpWidget(createSettingsDialog());

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.tap(find.text('Restart Chat'));
    await tester.pumpAndSettle();

    final messageState = Provider.of<MessageState>(
        tester.element(find.byType(MaterialApp)),
        listen: false);
    expect(messageState.messages.length, 2);
    expect(messageState.messages[0],
        {'text': 'Chat restarted', 'is_user_message': false});
    expect(messageState.messages[1],
        {'text': 'Welcome back', 'is_user_message': true});

    expect(find.byType(AlertDialog), findsNothing);
  });
  testWidgets('SettingsDialog closes when Close button is pressed',
      (WidgetTester tester) async {
    await tester.pumpWidget(createSettingsDialog());

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.tap(find.text('Close'));
    await tester.pumpAndSettle();

    expect(find.byType(AlertDialog), findsNothing);
  });
}
