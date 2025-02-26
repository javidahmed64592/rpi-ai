// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

class MenuItem extends StatelessWidget {
  final PageType page;
  const MenuItem({Key? key, required this.page}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    return ListTile(
      leading: Icon(page.icon),
      title: Text(page.title),
      onTap: () {
        page.handlePageChange(appState);
        Navigator.of(context).pop();
      },
      shape: Border(
        bottom: BorderSide(
            color: Theme.of(context).colorScheme.secondary, width: 1),
      ),
    );
  }
}
