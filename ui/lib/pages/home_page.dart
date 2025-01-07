import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/app_state.dart';
import 'package:ui/components/settings_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/login_page.dart';
import 'package:ui/pages/message_page.dart';
import 'dart:async';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Timer? timer;

  @override
  void initState() {
    super.initState();
    startCheckAPIAlive();
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  void startCheckAPIAlive() {
    timer = Timer.periodic(const Duration(minutes: 1), (timer) {
      final httpHelper = HttpHelper(client: http.Client());
      httpHelper.checkApiConnection(context);
    });
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);

    Widget getPage() {
      switch (appState.activePage) {
        case 'message':
          return const MessagePage();
        case 'login':
        default:
          return const LoginPage();
      }
    }

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Gemini'),
        leading: const SettingsButton(),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: getPage(),
        ),
      ),
    );
  }
}
