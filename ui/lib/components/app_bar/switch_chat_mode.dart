// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/state/app_state.dart';

class SwitchChatMode extends StatelessWidget {
  const SwitchChatMode({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);

    return IconButton(
      icon: const Icon(Icons.swap_horiz),
      onPressed: () {
        appState.toggleActivePage();
      },
    );
  }
}
