// Flutter imports:
import 'package:flutter/material.dart';

class SettingsState extends ChangeNotifier {
  String _model = '';
  String _systemInstruction = '';
  int _candidateCount = 1;
  int _maxOutputTokens = 1000;
  double _temperature = 1.0;

  String get model => _model;
  String get systemInstruction => _systemInstruction;
  int get candidateCount => _candidateCount;
  int get maxOutputTokens => _maxOutputTokens;
  double get temperature => _temperature;

  void updateConfig(Map<String, dynamic> config) {
    _model = config['model'];
    _systemInstruction = config['systemInstruction'];
    _candidateCount = config['candidateCount'];
    _maxOutputTokens = config['maxOutputTokens'];
    _temperature = config['temperature'];
    notifyListeners();
  }
}
