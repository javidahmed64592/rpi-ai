// Dart imports:
import 'dart:async';

// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/components/notifications.dart';
import 'package:ui/components/timeout_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/login_page.dart';
import 'package:ui/pages/message_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Timer? timer;
  final httpHelper = HttpHelper(client: http.Client());

  @override
  void initState() {
    super.initState();
    startCheckAPIAlive();
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  void checkApiAlive() {
    final appState = Provider.of<AppState>(context, listen: false);
    final notificationState =
        Provider.of<NotificationState>(context, listen: false);

    httpHelper.checkApiConnection('${appState.fullUrl}/').then((alive) {
      if (appState.activePage == 'login') {
        return;
      }
      if (!appState.connected && alive) {
        appState.setConnected(alive);
        notificationState.setNotificationInfo('API connection restored!');
      } else if (!appState.connected && !alive) {
        notificationState.setNotificationError('Failed to restore connection!');
      }
    }).catchError((error) {
      notificationState
          .setNotificationError('Error checking API connection: $error');
      appState.setConnected(false);
    });
  }

  void startCheckAPIAlive() {
    timer = Timer.periodic(const Duration(minutes: 1), (timer) {
      checkApiAlive();
    });
  }

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);
    final notificationState = Provider.of<NotificationState>(context);

    Widget getPage() {
      switch (appState.activePage) {
        case 'message':
          return MessagePage(httpHelper: httpHelper);
        case 'login':
        default:
          return LoginPage(httpHelper: httpHelper);
      }
    }

    Widget notification() {
      onClose() {
        return () {
          notificationState.clearNotification();
        };
      }

      switch (notificationState.notificationState) {
        case 'error':
          return NotificationError(
            message:
                notificationState.notificationMessage ?? 'An error occurred.',
            onClose: onClose(),
          );
        case 'warning':
          return NotificationWarning(
            message:
                notificationState.notificationMessage ?? 'A warning occurred.',
            onClose: onClose(),
          );
        case 'info':
          return NotificationInfo(
            message: notificationState.notificationMessage ??
                'This is an informational message.',
            onClose: onClose(),
          );
        default:
          return Container();
      }
    }

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Gemini'),
        leading: appState.activePage != 'login' ? const SettingsButton() : null,
        actions: appState.activePage != 'login'
            ? [
                const LogoutButton(),
              ]
            : null,
      ),
      body: Stack(
        children: [
          Center(
            child: Padding(
              padding: const EdgeInsets.all(10),
              child: getPage(),
            ),
          ),
          if (notificationState.notificationState != null)
            Positioned(
              bottom: 0,
              left: MediaQuery.of(context).size.width * 0.1,
              right: MediaQuery.of(context).size.width * 0.1,
              child: notification(),
            ),
          if (!appState.connected && appState.activePage == 'message')
            TimeoutDialog(retryConnection: checkApiAlive),
        ],
      ),
    );
  }
}
