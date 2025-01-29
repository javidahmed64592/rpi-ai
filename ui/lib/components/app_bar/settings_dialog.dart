// Flutter imports:
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/state/settings_state.dart';

class SettingsDialog extends StatelessWidget {
  const SettingsDialog({super.key});

  @override
  Widget build(BuildContext context) {
    final settingsState = Provider.of<SettingsState>(context);

    final TextEditingController modelController =
        TextEditingController(text: settingsState.model);
    final TextEditingController systemInstructionController =
        TextEditingController(text: settingsState.systemInstruction);
    final TextEditingController candidateCountController =
        TextEditingController(text: settingsState.candidateCount.toString());
    final TextEditingController maxOutputTokensController =
        TextEditingController(text: settingsState.maxOutputTokens.toString());
    final TextEditingController temperatureController =
        TextEditingController(text: settingsState.temperature.toString());

    Widget closeButton() {
      return TextButton(
        child: const Text('Close'),
        onPressed: () {
          Navigator.of(context).pop();
        },
      );
    }

    Widget updateButton() {
      return TextButton(
        child: const Text('Update'),
        onPressed: () {
          settingsState.setModel(modelController.text);
          settingsState.setSystemInstruction(systemInstructionController.text);
          settingsState
              .setCandidateCount(int.parse(candidateCountController.text));
          settingsState
              .setMaxOutputTokens(int.parse(maxOutputTokensController.text));
          settingsState
              .setTemperature(double.parse(temperatureController.text));
          Navigator.of(context).pop();
        },
      );
    }

    return AlertDialog(
      title: const Text('Settings'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          TextField(
            controller: modelController,
            decoration: const InputDecoration(labelText: 'Model'),
          ),
          TextField(
            controller: systemInstructionController,
            decoration: const InputDecoration(labelText: 'System Instruction'),
          ),
          TextField(
            controller: candidateCountController,
            decoration: const InputDecoration(labelText: 'Candidate Count'),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: maxOutputTokensController,
            decoration: const InputDecoration(labelText: 'Max Output Tokens'),
            keyboardType: TextInputType.number,
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'[0-9]')),
              LengthLimitingTextInputFormatter(4),
            ],
            onChanged: (value) {
              int intValue = int.tryParse(value) ?? 10;
              if (intValue < 10) {
                maxOutputTokensController.text = '10';
              } else if (intValue > 2000) {
                maxOutputTokensController.text = '2000';
              }
            },
          ),
          TextField(
            controller: temperatureController,
            decoration: const InputDecoration(labelText: 'Temperature'),
            keyboardType: TextInputType.number,
            inputFormatters: [
              FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d*')),
            ],
            onChanged: (value) {
              double doubleValue = double.tryParse(value) ?? 0.1;
              if (doubleValue < 0.1) {
                temperatureController.text = '0.1';
              } else if (doubleValue > 2.0) {
                temperatureController.text = '2.0';
              }
            },
          ),
        ],
      ),
      actions: <Widget>[
        closeButton(),
        updateButton(),
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
