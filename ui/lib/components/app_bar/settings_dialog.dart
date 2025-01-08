import 'package:flutter/material.dart';

class SettingsDialog extends StatelessWidget {
  const SettingsDialog({super.key});

  @override
  Widget build(BuildContext context) {
    Widget closeButton() {
      return TextButton(
        child: const Text('Close'),
        onPressed: () {
          Navigator.of(context).pop();
        },
      );
    }

    return AlertDialog(
      title: const Text('Settings'),
      content: const Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[],
      ),
      actions: <Widget>[
        closeButton(),
      ],
    );
  }
}

class SettingsButton extends StatelessWidget {
  const SettingsButton({super.key});

  void showSettingsDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return const SettingsDialog();
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.settings),
      onPressed: () => showSettingsDialog(context),
    );
  }
}
