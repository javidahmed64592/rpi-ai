// Package imports:
import 'package:shared_preferences/shared_preferences.dart';

class DataStorageHelper {
  static Future<Map<String, dynamic>> loadAppState() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String ip = prefs.getString('ip') ?? '127.0.0.1';
    int port = prefs.getInt('port') ?? 443;
    String authToken = prefs.getString('authToken') ?? '';
    return {'ip': ip, 'port': port, 'authToken': authToken};
  }

  static Future<void> saveAppState(
      String ip, int port, String authToken) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('ip', ip);
    await prefs.setInt('port', port);
    await prefs.setString('authToken', authToken);
  }
}
