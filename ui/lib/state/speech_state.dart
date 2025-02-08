// Flutter imports:
import 'package:flutter/material.dart';

class SpeechState extends ChangeNotifier {
  bool _microphonePermissionGranted = false;
  bool _isRecording = false;
  bool _isBusy = false;

  bool get microphonePermissionGranted => _microphonePermissionGranted;
  bool get isRecording => _isRecording;
  bool get isBusy => _isBusy;

  void setMicrophonePermissionGranted(bool granted) {
    _microphonePermissionGranted = granted;
    notifyListeners();
  }

  void setIsRecording(bool recording) {
    _isRecording = recording;
    notifyListeners();
  }

  void setIsBusy(bool busy) {
    _isBusy = busy;
    notifyListeners();
  }
}
