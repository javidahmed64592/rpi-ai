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

  void setModel(String newModel) {
    _model = newModel;
    notifyListeners();
  }

  void setSystemInstruction(String newSystemInstruction) {
    _systemInstruction = newSystemInstruction;
    notifyListeners();
  }

  void setCandidateCount(int newCandidateCount) {
    _candidateCount = newCandidateCount;
    notifyListeners();
  }

  void setMaxOutputTokens(int newMaxOutputTokens) {
    _maxOutputTokens = newMaxOutputTokens;
    notifyListeners();
  }

  void setTemperature(double newTemperature) {
    _temperature = newTemperature;
    notifyListeners();
  }
}
