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
import 'package:ui/types.dart';

class LoginPage extends StatefulWidget {
  final HttpHelper? httpHelper;

  const LoginPage({super.key, this.httpHelper});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  late AppState appState;
  late MessageState messageState;
  late NotificationState notificationState;
  late SettingsState settingsState;
  late TextEditingController ipController;
  late TextEditingController portController;
  late TextEditingController authTokenController;
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    appState = Provider.of<AppState>(context, listen: false);
    messageState = Provider.of<MessageState>(context, listen: false);
    notificationState = Provider.of<NotificationState>(context, listen: false);
    settingsState = Provider.of<SettingsState>(context, listen: false);
    httpHelper = widget.httpHelper ?? HttpHelper();
    ipController = TextEditingController(text: appState.ip);
    portController = TextEditingController(text: appState.port.toString());
    authTokenController = TextEditingController(text: appState.authToken);
  }

  @override
  Widget build(BuildContext context) {
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

    Widget authTokenTextField() {
      return TextField(
        controller: authTokenController,
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Authentication Token',
        ),
        onChanged: appState.setAuthToken,
      );
    }

    Widget connectButton() {
      return ElevatedButton(
        child: const Text('Connect'),
        onPressed: () async {
          try {
            final Map<String, dynamic> message = await httpHelper
                .getLoginResponse(appState.fullUrl, appState.authToken);
            final Map<String, dynamic> config = await httpHelper.getConfig(
                appState.fullUrl, appState.authToken);

            if (message.isNotEmpty) {
              settingsState.updateConfig(config);
              appState.setConnected(true);
              messageState.initialiseChat(message);
              appState.setActivePage(PageType.chat);
              notificationState.clearNotification();
            }
          } catch (e) {
            notificationState.setNotificationError('Failed to connect: $e');
          }
        },
      );
    }

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            ipTextField(),
            const SizedBox(height: 10),
            portTextField(),
            const SizedBox(height: 10),
            authTokenTextField(),
            const SizedBox(height: 20),
            connectButton(),
          ],
        ),
      ),
    );
  }
}
