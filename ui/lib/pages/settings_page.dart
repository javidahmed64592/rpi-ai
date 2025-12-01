// Flutter imports:
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';

class SettingsPage extends StatefulWidget {
  final HttpHelper? httpHelper;
  const SettingsPage({
    Key? key,
    this.httpHelper,
  }) : super(key: key);

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  late AppState appState;
  late NotificationState notificationState;
  late MessageState messageState;
  late SettingsState settingsState;
  late HttpHelper httpHelper;

  late TextEditingController modelController;
  late TextEditingController systemInstructionController;
  late TextEditingController maxOutputTokensController;
  late TextEditingController temperatureController;

  @override
  void initState() {
    super.initState();
    appState = Provider.of<AppState>(context, listen: false);
    notificationState = Provider.of<NotificationState>(context, listen: false);
    messageState = Provider.of<MessageState>(context, listen: false);
    settingsState = Provider.of<SettingsState>(context, listen: false);
    httpHelper = widget.httpHelper ?? HttpHelper();
    modelController = TextEditingController(text: settingsState.model);
    systemInstructionController =
        TextEditingController(text: settingsState.systemInstruction);
    maxOutputTokensController =
        TextEditingController(text: settingsState.maxOutputTokens.toString());
    temperatureController =
        TextEditingController(text: settingsState.temperature.toString());
  }

  Widget modelTextField() {
    return TextField(
      controller: modelController,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'Model',
      ),
    );
  }

  Widget systemInstructionTextField() {
    return TextField(
      controller: systemInstructionController,
      maxLines: 7,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'System Instruction',
      ),
    );
  }

  Widget maxOutputTokensTextField() {
    return TextField(
      controller: maxOutputTokensController,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'Max Output Tokens',
      ),
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
    );
  }

  Widget temperatureTextField() {
    return TextField(
      controller: temperatureController,
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'Temperature',
      ),
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
    );
  }

  Widget updateButton() {
    return Expanded(
      child: ElevatedButton(
        child: const Text('Update'),
        onPressed: () {
          final Map<String, dynamic> config = {
            'model': modelController.text,
            'system_instruction': systemInstructionController.text,
            'max_output_tokens': int.parse(maxOutputTokensController.text),
            'temperature': double.parse(temperatureController.text),
          };

          try {
            httpHelper
                .postConfig(appState.fullUrl, appState.authToken, config)
                .then((messages) {
              settingsState.postConfig({
                'model': config['model'],
                'systemInstruction': config['system_instruction'],
                'maxOutputTokens': config['max_output_tokens'],
                'temperature': config['temperature'],
              });
              messageState.initialiseChat(messages);
              notificationState
                  .setNotificationInfo('AI configuration updated!');
            });
          } catch (error) {
            notificationState
                .setNotificationError('Error updating settings: $error');
          }
        },
      ),
    );
  }

  Widget restartChatButton() {
    return Expanded(
      child: ElevatedButton(
        child: const Text('Restart Chat'),
        onPressed: () {
          try {
            httpHelper
                .postRestartChat(appState.fullUrl, appState.authToken)
                .then((messages) {
              messageState.initialiseChat(messages);
              notificationState.setNotificationInfo('Chat restarted!');
            });
          } catch (error) {
            notificationState
                .setNotificationError('Error restarting chat: $error');
          }
        },
      ),
    );
  }

  Widget logoutButton() {
    return Expanded(
      child: ElevatedButton(
        child: const Text('Logout'),
        onPressed: () {
          appState.setConnected(false);
          appState.setPageLogin();
          notificationState.clearNotification();
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            modelTextField(),
            const SizedBox(height: 10),
            systemInstructionTextField(),
            const SizedBox(height: 10),
            maxOutputTokensTextField(),
            const SizedBox(height: 10),
            temperatureTextField(),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                updateButton(),
                const SizedBox(width: 10),
                restartChatButton(),
                const SizedBox(width: 10),
                logoutButton(),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
