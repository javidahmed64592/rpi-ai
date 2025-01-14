// Flutter imports:
import 'package:flutter/material.dart';

class NotificationPopup extends StatelessWidget {
  final String message;
  final Color backgroundColor;
  final IconData icon;
  final VoidCallback? onClose;

  const NotificationPopup({
    Key? key,
    required this.message,
    required this.backgroundColor,
    required this.icon,
    this.onClose,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(10.0),
      padding: const EdgeInsets.all(15.0),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(10.0),
        boxShadow: const [
          BoxShadow(
            color: Colors.black26,
            blurRadius: 10.0,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            color: Colors.white,
          ),
          const SizedBox(width: 10.0),
          Expanded(
            child: Text(
              message.trim(),
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16.0,
              ),
            ),
          ),
          if (onClose != null)
            GestureDetector(
              onTap: onClose,
              child: const Icon(
                Icons.close,
                color: Colors.white,
              ),
            ),
        ],
      ),
    );
  }
}

class NotificationError extends StatelessWidget {
  final String message;
  final VoidCallback? onClose;

  const NotificationError({Key? key, required this.message, this.onClose})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return NotificationPopup(
      message: message,
      backgroundColor: Theme.of(context).colorScheme.error,
      icon: Icons.error,
      onClose: onClose,
    );
  }
}

class NotificationWarning extends StatelessWidget {
  final String message;
  final VoidCallback? onClose;

  const NotificationWarning({Key? key, required this.message, this.onClose})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return NotificationPopup(
      message: message,
      backgroundColor: Theme.of(context).colorScheme.secondary,
      icon: Icons.warning,
      onClose: onClose,
    );
  }
}

class NotificationInfo extends StatelessWidget {
  final String message;
  final VoidCallback? onClose;

  const NotificationInfo({Key? key, required this.message, this.onClose})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return NotificationPopup(
      message: message,
      backgroundColor: Theme.of(context).colorScheme.primary,
      icon: Icons.info,
      onClose: onClose,
    );
  }
}
