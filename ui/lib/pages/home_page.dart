import 'package:flutter/material.dart';
import '../components/settings_dialog.dart';
import '../pages/message_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Gemini'),
        leading: const SettingsButton(),
      ),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(10),
          child: MessagePage(),
        ),
      ),
    );
  }
}
