import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../app_state.dart';

class SettingsDialog extends StatelessWidget {
  const SettingsDialog({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context, listen: false);
    final TextEditingController ipController =
        TextEditingController(text: appState.ip);
    final TextEditingController portController =
        TextEditingController(text: appState.port.toString());

    Widget ipTextField() {
      return TextField(
        controller: ipController,
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'IP',
        ),
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        inputFormatters: <TextInputFormatter>[
          FilteringTextInputFormatter.allow(RegExp(r'[0-9.]'))
        ],
        onChanged: appState.setIp,
      );
    }

    Widget portTextField() {
      return TextField(
        controller: portController,
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Port',
        ),
        keyboardType: TextInputType.number,
        inputFormatters: <TextInputFormatter>[
          FilteringTextInputFormatter.digitsOnly
        ],
        onChanged: (String value) {
          if (value.isNotEmpty) {
            appState.setPort(int.parse(value));
          }
        },
      );
    }

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
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          ipTextField(),
          const SizedBox(height: 10),
          portTextField(),
        ],
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
