// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/switch_chat_mode.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final AppState appState;

  const CustomAppBar({Key? key, required this.appState}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      title: Text(appState.activePage.title),
      leading:
          appState.activePage != PageType.login ? const SwitchChatMode() : null,
      actions: appState.activePage != PageType.login
          ? [
              const LogoutButton(),
            ]
          : null,
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
