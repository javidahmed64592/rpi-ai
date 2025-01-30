// Flutter imports:
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// Package imports:
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';

class SettingsDialog extends StatelessWidget {
  final HttpHelper? httpHelper;

  const SettingsDialog({super.key, this.httpHelper});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final messageState = Provider.of<MessageState>(context);
    final notificationState = Provider.of<NotificationState>(context);
    final settingsState = Provider.of<SettingsState>(context);
    final httpHelper = this.httpHelper ?? HttpHelper(client: http.Client());

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
          final Map<String, dynamic> config = {
            'model': modelController.text,
            'system_instruction': systemInstructionController.text,
            'candidate_count': int.parse(candidateCountController.text),
            'max_output_tokens': int.parse(maxOutputTokensController.text),
            'temperature': double.parse(temperatureController.text),
          };

          try {
            httpHelper
                .updateConfig(appState.fullUrl, appState.authToken, config)
                .then((value) {
              settingsState.updateConfig({
                'model': config['model'],
                'systemInstruction': config['system_instruction'],
                'candidateCount': config['candidate_count'],
                'maxOutputTokens': config['max_output_tokens'],
                'temperature': config['temperature'],
              });
              messageState.initialiseChat(value);
            });
          } catch (error) {
            notificationState
                .setNotificationError('Error updating settings: $error');
          }

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
