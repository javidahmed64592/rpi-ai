import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/app_state.dart';

class LogoutButton extends StatelessWidget {
  const LogoutButton({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context, listen: false);

    return IconButton(
      icon: const Icon(Icons.logout),
      onPressed: () {
        appState.setActivePage('login');
      },
    );
  }
}
