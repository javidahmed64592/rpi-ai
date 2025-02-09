// Flutter imports:
import 'package:flutter/material.dart';

class StatusDisplayBox extends StatelessWidget {
  final String primaryMessage;
  final String secondaryMessage;
  final IconData primaryIcon;
  final IconData secondaryIcon;
  final Color primaryColor;
  final Color secondaryColor;
  final bool showPrimary;

  const StatusDisplayBox({
    Key? key,
    required this.primaryMessage,
    required this.secondaryMessage,
    required this.primaryIcon,
    required this.secondaryIcon,
    required this.primaryColor,
    required this.secondaryColor,
    required this.showPrimary,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final color = showPrimary ? primaryColor : secondaryColor;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border.all(color: color),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            showPrimary ? primaryIcon : secondaryIcon,
            color: color,
          ),
          const SizedBox(width: 8),
          Text(
            showPrimary ? primaryMessage : secondaryMessage,
            style: TextStyle(color: color),
          ),
        ],
      ),
    );
  }
}
