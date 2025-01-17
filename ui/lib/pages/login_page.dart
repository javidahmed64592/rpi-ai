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

class LoginPage extends StatefulWidget {
  final HttpHelper httpHelper;

  const LoginPage({super.key, required this.httpHelper});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  late TextEditingController ipController;
  late TextEditingController portController;
  late TextEditingController authTokenController;
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    final appState = Provider.of<AppState>(context, listen: false);
    httpHelper = widget.httpHelper;
    ipController = TextEditingController(text: appState.ip);
    portController = TextEditingController(text: appState.port.toString());
    authTokenController = TextEditingController(text: appState.authToken);
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context, listen: false);
    final messageState = Provider.of<MessageState>(context, listen: false);
    final notificationState =
        Provider.of<NotificationState>(context, listen: false);

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
            if (message.isNotEmpty) {
              appState.setConnected(true);
              messageState.clearMessages();
              messageState.addMessage(message);
              appState.setActivePage('message');
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
