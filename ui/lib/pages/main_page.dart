// Dart imports:
import 'dart:async';

// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/components/notifications.dart';
import 'package:ui/components/timeout_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/text_page.dart';
import 'package:ui/pages/login_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/types.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  Timer? timer;
  final httpHelper = HttpHelper();

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
      if (appState.activePage == PageType.login) {
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
        case PageType.text:
          return const TextPage();
        case PageType.login:
        default:
          return const LoginPage();
      }
    }

    Widget notification() {
      onClose() {
        return () {
          notificationState.clearNotification();
        };
      }

      switch (notificationState.notificationState) {
        case NotificationType.error:
          return NotificationError(
            message:
                notificationState.notificationMessage ?? 'An error occurred.',
            onClose: onClose(),
          );
        case NotificationType.warning:
          return NotificationWarning(
            message:
                notificationState.notificationMessage ?? 'A warning occurred.',
            onClose: onClose(),
          );
        case NotificationType.info:
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
      appBar: const CustomAppBar(),
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
          if (!appState.connected && appState.activePage != PageType.login)
            TimeoutDialog(retryConnection: checkApiAlive),
        ],
      ),
    );
  }
}
