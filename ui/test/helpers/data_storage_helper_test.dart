// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Project imports:
import 'package:ui/helpers/data_storage_helper.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('saveAppState saves data correctly', () async {
    SharedPreferences.setMockInitialValues({});
    await DataStorageHelper.saveAppState('192.168.1.1', 8080, 'testToken');

    SharedPreferences prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('ip'), '192.168.1.1');
    expect(prefs.getInt('port'), 8080);
    expect(prefs.getString('authToken'), 'testToken');
  });

  test('loadAppState loads data correctly', () async {
    SharedPreferences.setMockInitialValues({
      'ip': '192.168.1.1',
      'port': 8080,
      'authToken': 'testToken',
    });

    Map<String, dynamic> appState = await DataStorageHelper.loadAppState();
    expect(appState['ip'], '192.168.1.1');
    expect(appState['port'], 8080);
    expect(appState['authToken'], 'testToken');
  });

  test('loadAppState returns default values when no data is saved', () async {
    SharedPreferences.setMockInitialValues({});

    Map<String, dynamic> appState = await DataStorageHelper.loadAppState();
    expect(appState['ip'], '127.0.0.1');
    expect(appState['port'], 443);
    expect(appState['authToken'], '');
  });
}
