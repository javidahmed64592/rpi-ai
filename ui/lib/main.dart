// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/pages/main_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';
import 'package:ui/state/speech_state.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => AppState()),
        ChangeNotifierProvider(create: (context) => MessageState()),
        ChangeNotifierProvider(create: (context) => NotificationState()),
        ChangeNotifierProvider(create: (context) => SettingsState()),
        ChangeNotifierProvider(create: (context) => SpeechState()),
      ],
      child: const AIApp(),
    ),
  );
}

class AIApp extends StatelessWidget {
  const AIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Raspberry Pi AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color.fromARGB(255, 46, 172, 73),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const MainPage(),
    );
  }
}
