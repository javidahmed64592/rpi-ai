// Dart imports:
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:audioplayers/audioplayers.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';

// Project imports:
import 'package:ui/components/audio/status_display_box.dart';
import 'package:ui/components/conversation/speech_input.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/speech_state.dart';

class SpeechPage extends StatefulWidget {
  final HttpHelper? httpHelper;
  const SpeechPage({
    Key? key,
    this.httpHelper,
  }) : super(key: key);

  @override
  State<SpeechPage> createState() => _SpeechPageState();
}

class _SpeechPageState extends State<SpeechPage> {
  final Record _audioRecorder = Record();
  final AudioPlayer _audioPlayer = AudioPlayer();
  late AppState appState;
  late NotificationState notificationState;
  late SpeechState speechState;
  late HttpHelper httpHelper;

  Future<void> _requestPermissions() async {
    if (await Permission.microphone.request().isGranted) {
      speechState.setMicrophonePermissionGranted(true);
      notificationState.setNotificationInfo('Permission granted!');
    } else {
      notificationState
          .setNotificationError('Microphone permission is required.');
    }
  }

  Future<void> _checkPermissions() async {
    if (await Permission.microphone.isGranted) {
      speechState.setMicrophonePermissionGranted(true);
    } else {
      await _requestPermissions();
    }
  }

  void _startRecording() async {
    try {
      speechState.setIsRecording(true);
      await _audioRecorder.start(
        encoder: AudioEncoder.opus,
        samplingRate: 48000,
      );
    } catch (e) {
      notificationState.setNotificationError('Error starting recording: $e');
    }
  }

  void _stopRecording() async {
    try {
      final path = await _audioRecorder.stop();
      speechState.setIsRecording(false);
      appState.setIsBusy(true);

      if (path == null) {
        notificationState.setNotificationError('No audio recorded.');
        return;
      }

      final Uint8List audioBytes = await File(path).readAsBytes();
      final response = await httpHelper.postMessageAudio(
          appState.fullUrl, appState.authToken, audioBytes);

      if (response['bytes'] != null) {
        final decodedBytes = BytesSource(base64Decode(response['bytes']));
        await _audioPlayer.play(decodedBytes);
        _audioPlayer.onPlayerComplete.listen((event) {
          appState.setIsBusy(false);
        });
      } else {
        throw Exception(response['text']);
      }
    } catch (e) {
      notificationState.setNotificationError('Error stopping recording: $e');
      appState.setIsBusy(false);
    }
  }

  @override
  void initState() {
    super.initState();
    appState = Provider.of<AppState>(context, listen: false);
    notificationState = Provider.of<NotificationState>(context, listen: false);
    speechState = Provider.of<SpeechState>(context, listen: false);
    httpHelper = widget.httpHelper ?? HttpHelper();
    _checkPermissions();
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: <Widget>[
          Row(
            children: [
              Expanded(
                child: Consumer<AppState>(
                  builder: (context, appState, child) {
                    return Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: StatusDisplayBox(
                        primaryMessage: 'Ready',
                        secondaryMessage: 'Thinking...',
                        primaryIcon: Icons.check_circle,
                        secondaryIcon: Icons.hourglass_empty,
                        primaryColor: Theme.of(context).colorScheme.onSurface,
                        secondaryColor: Theme.of(context).colorScheme.tertiary,
                        showPrimary: !appState.isBusy,
                      ),
                    );
                  },
                ),
              ),
              Expanded(
                child: Consumer<SpeechState>(
                  builder: (context, speechState, child) {
                    return Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: StatusDisplayBox(
                        primaryMessage: 'Recording...',
                        secondaryMessage: 'Not recording',
                        primaryIcon: Icons.mic,
                        secondaryIcon: Icons.mic_off,
                        primaryColor: Theme.of(context).colorScheme.primary,
                        secondaryColor: Theme.of(context).colorScheme.error,
                        showPrimary: speechState.isRecording,
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
          Expanded(
            child: Center(
              child: SpeechInput(
                onRequestPermissions: _requestPermissions,
                onStartRecording: _startRecording,
                onStopRecording: _stopRecording,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
