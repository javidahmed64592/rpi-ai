// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/components/drawer/menu_item.dart';
import 'package:ui/types.dart';

class MenuDrawer extends StatelessWidget {
  const MenuDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primaryContainer,
            ),
            child: Text(
              'Switch page',
              style: TextStyle(
                color: Theme.of(context).colorScheme.onPrimaryContainer,
                fontSize: 24,
              ),
            ),
          ),
          const MenuItem(page: PageType.text),
          const MenuItem(page: PageType.speech),
          const MenuItem(page: PageType.settings),
        ],
      ),
    );
  }
}
