// Mocks generated by Mockito 5.4.4 from annotations
// in ui/test/components/conversation/text_input_test.dart.
// Do not manually edit this file.

// ignore_for_file: no_leading_underscores_for_library_prefixes

// Dart imports:
import 'dart:async' as _i4;
import 'dart:typed_data' as _i5;
import 'dart:ui' as _i9;

// Package imports:
import 'package:http/http.dart' as _i2;
import 'package:mockito/mockito.dart' as _i1;
import 'package:mockito/src/dummies.dart' as _i7;

// Project imports:
import 'package:ui/helpers/http_helper.dart' as _i3;
import 'package:ui/state/app_state.dart' as _i6;
import 'package:ui/state/message_state.dart' as _i10;
import 'package:ui/state/notification_state.dart' as _i11;
import 'package:ui/types.dart' as _i8;

// ignore_for_file: type=lint
// ignore_for_file: avoid_redundant_argument_values
// ignore_for_file: avoid_setters_without_getters
// ignore_for_file: comment_references
// ignore_for_file: deprecated_member_use
// ignore_for_file: deprecated_member_use_from_same_package
// ignore_for_file: implementation_imports
// ignore_for_file: invalid_use_of_visible_for_testing_member
// ignore_for_file: prefer_const_constructors
// ignore_for_file: unnecessary_parenthesis
// ignore_for_file: camel_case_types
// ignore_for_file: subtype_of_sealed_class

class _FakeClient_0 extends _i1.SmartFake implements _i2.Client {
  _FakeClient_0(
    Object parent,
    Invocation parentInvocation,
  ) : super(
          parent,
          parentInvocation,
        );
}

class _FakeResponse_1 extends _i1.SmartFake implements _i2.Response {
  _FakeResponse_1(
    Object parent,
    Invocation parentInvocation,
  ) : super(
          parent,
          parentInvocation,
        );
}

/// A class which mocks [HttpHelper].
///
/// See the documentation for Mockito's code generation for more information.
class MockHttpHelper extends _i1.Mock implements _i3.HttpHelper {
  MockHttpHelper() {
    _i1.throwOnMissingStub(this);
  }

  @override
  _i2.Client get client => (super.noSuchMethod(
        Invocation.getter(#client),
        returnValue: _FakeClient_0(
          this,
          Invocation.getter(#client),
        ),
      ) as _i2.Client);

  @override
  _i4.Future<_i2.Response> getResponseFromUri(
    String? uri,
    Map<String, String>? headers,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #getResponseFromUri,
          [
            uri,
            headers,
          ],
        ),
        returnValue: _i4.Future<_i2.Response>.value(_FakeResponse_1(
          this,
          Invocation.method(
            #getResponseFromUri,
            [
              uri,
              headers,
            ],
          ),
        )),
      ) as _i4.Future<_i2.Response>);

  @override
  _i4.Future<_i2.Response> postResponseToUri(
    String? uri,
    Map<String, String>? headers,
    String? body,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #postResponseToUri,
          [
            uri,
            headers,
            body,
          ],
        ),
        returnValue: _i4.Future<_i2.Response>.value(_FakeResponse_1(
          this,
          Invocation.method(
            #postResponseToUri,
            [
              uri,
              headers,
              body,
            ],
          ),
        )),
      ) as _i4.Future<_i2.Response>);

  @override
  _i4.Future<bool> checkApiConnection(String? url) => (super.noSuchMethod(
        Invocation.method(
          #checkApiConnection,
          [url],
        ),
        returnValue: _i4.Future<bool>.value(false),
      ) as _i4.Future<bool>);

  @override
  _i4.Future<List<Map<String, dynamic>>> getLoginResponse(
    String? url,
    String? authToken,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #getLoginResponse,
          [
            url,
            authToken,
          ],
        ),
        returnValue: _i4.Future<List<Map<String, dynamic>>>.value(
            <Map<String, dynamic>>[]),
      ) as _i4.Future<List<Map<String, dynamic>>>);

  @override
  _i4.Future<List<Map<String, dynamic>>> postRestartChat(
    String? url,
    String? authToken,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #postRestartChat,
          [
            url,
            authToken,
          ],
        ),
        returnValue: _i4.Future<List<Map<String, dynamic>>>.value(
            <Map<String, dynamic>>[]),
      ) as _i4.Future<List<Map<String, dynamic>>>);

  @override
  _i4.Future<Map<String, dynamic>> getConfig(
    String? url,
    String? authToken,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #getConfig,
          [
            url,
            authToken,
          ],
        ),
        returnValue:
            _i4.Future<Map<String, dynamic>>.value(<String, dynamic>{}),
      ) as _i4.Future<Map<String, dynamic>>);

  @override
  _i4.Future<List<Map<String, dynamic>>> updateConfig(
    String? url,
    String? authToken,
    Map<String, dynamic>? config,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #updateConfig,
          [
            url,
            authToken,
            config,
          ],
        ),
        returnValue: _i4.Future<List<Map<String, dynamic>>>.value(
            <Map<String, dynamic>>[]),
      ) as _i4.Future<List<Map<String, dynamic>>>);

  @override
  _i4.Future<Map<String, dynamic>> chat(
    String? url,
    String? authToken,
    String? message,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #chat,
          [
            url,
            authToken,
            message,
          ],
        ),
        returnValue:
            _i4.Future<Map<String, dynamic>>.value(<String, dynamic>{}),
      ) as _i4.Future<Map<String, dynamic>>);

  @override
  _i4.Future<Map<String, dynamic>> sendAudio(
    String? url,
    String? authToken,
    _i5.Uint8List? audioBytes,
  ) =>
      (super.noSuchMethod(
        Invocation.method(
          #sendAudio,
          [
            url,
            authToken,
            audioBytes,
          ],
        ),
        returnValue:
            _i4.Future<Map<String, dynamic>>.value(<String, dynamic>{}),
      ) as _i4.Future<Map<String, dynamic>>);
}

/// A class which mocks [AppState].
///
/// See the documentation for Mockito's code generation for more information.
class MockAppState extends _i1.Mock implements _i6.AppState {
  MockAppState() {
    _i1.throwOnMissingStub(this);
  }

  @override
  String get ip => (super.noSuchMethod(
        Invocation.getter(#ip),
        returnValue: _i7.dummyValue<String>(
          this,
          Invocation.getter(#ip),
        ),
      ) as String);

  @override
  int get port => (super.noSuchMethod(
        Invocation.getter(#port),
        returnValue: 0,
      ) as int);

  @override
  String get fullUrl => (super.noSuchMethod(
        Invocation.getter(#fullUrl),
        returnValue: _i7.dummyValue<String>(
          this,
          Invocation.getter(#fullUrl),
        ),
      ) as String);

  @override
  String get authToken => (super.noSuchMethod(
        Invocation.getter(#authToken),
        returnValue: _i7.dummyValue<String>(
          this,
          Invocation.getter(#authToken),
        ),
      ) as String);

  @override
  _i8.PageType get activePage => (super.noSuchMethod(
        Invocation.getter(#activePage),
        returnValue: _i8.PageType.login,
      ) as _i8.PageType);

  @override
  bool get connected => (super.noSuchMethod(
        Invocation.getter(#connected),
        returnValue: false,
      ) as bool);

  @override
  bool get isBusy => (super.noSuchMethod(
        Invocation.getter(#isBusy),
        returnValue: false,
      ) as bool);

  @override
  bool get hasListeners => (super.noSuchMethod(
        Invocation.getter(#hasListeners),
        returnValue: false,
      ) as bool);

  @override
  void setIp(String? newIp) => super.noSuchMethod(
        Invocation.method(
          #setIp,
          [newIp],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setPort(int? newPort) => super.noSuchMethod(
        Invocation.method(
          #setPort,
          [newPort],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setAuthToken(String? newAuthToken) => super.noSuchMethod(
        Invocation.method(
          #setAuthToken,
          [newAuthToken],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setActivePage(_i8.PageType? newPage) => super.noSuchMethod(
        Invocation.method(
          #setActivePage,
          [newPage],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void toggleActivePage() => super.noSuchMethod(
        Invocation.method(
          #toggleActivePage,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setConnected(bool? newConnected) => super.noSuchMethod(
        Invocation.method(
          #setConnected,
          [newConnected],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setIsBusy(bool? busy) => super.noSuchMethod(
        Invocation.method(
          #setIsBusy,
          [busy],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void addListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #addListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void removeListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #removeListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void dispose() => super.noSuchMethod(
        Invocation.method(
          #dispose,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void notifyListeners() => super.noSuchMethod(
        Invocation.method(
          #notifyListeners,
          [],
        ),
        returnValueForMissingStub: null,
      );
}

/// A class which mocks [MessageState].
///
/// See the documentation for Mockito's code generation for more information.
class MockMessageState extends _i1.Mock implements _i10.MessageState {
  MockMessageState() {
    _i1.throwOnMissingStub(this);
  }

  @override
  List<Map<String, dynamic>> get messages => (super.noSuchMethod(
        Invocation.getter(#messages),
        returnValue: <Map<String, dynamic>>[],
      ) as List<Map<String, dynamic>>);

  @override
  bool get hasListeners => (super.noSuchMethod(
        Invocation.getter(#hasListeners),
        returnValue: false,
      ) as bool);

  @override
  void addMessage(Map<String, dynamic>? message) => super.noSuchMethod(
        Invocation.method(
          #addMessage,
          [message],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void addMessages(List<Map<String, dynamic>>? messages) => super.noSuchMethod(
        Invocation.method(
          #addMessages,
          [messages],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void clearMessages() => super.noSuchMethod(
        Invocation.method(
          #clearMessages,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void removeLastMessage() => super.noSuchMethod(
        Invocation.method(
          #removeLastMessage,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void initialiseChat(List<Map<String, dynamic>>? messages) =>
      super.noSuchMethod(
        Invocation.method(
          #initialiseChat,
          [messages],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void addListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #addListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void removeListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #removeListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void dispose() => super.noSuchMethod(
        Invocation.method(
          #dispose,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void notifyListeners() => super.noSuchMethod(
        Invocation.method(
          #notifyListeners,
          [],
        ),
        returnValueForMissingStub: null,
      );
}

/// A class which mocks [NotificationState].
///
/// See the documentation for Mockito's code generation for more information.
class MockNotificationState extends _i1.Mock implements _i11.NotificationState {
  MockNotificationState() {
    _i1.throwOnMissingStub(this);
  }

  @override
  bool get hasListeners => (super.noSuchMethod(
        Invocation.getter(#hasListeners),
        returnValue: false,
      ) as bool);

  @override
  void setNotificationError(String? message) => super.noSuchMethod(
        Invocation.method(
          #setNotificationError,
          [message],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setNotificationWarning(String? message) => super.noSuchMethod(
        Invocation.method(
          #setNotificationWarning,
          [message],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void setNotificationInfo(String? message) => super.noSuchMethod(
        Invocation.method(
          #setNotificationInfo,
          [message],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void clearNotification() => super.noSuchMethod(
        Invocation.method(
          #clearNotification,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void addListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #addListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void removeListener(_i9.VoidCallback? listener) => super.noSuchMethod(
        Invocation.method(
          #removeListener,
          [listener],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void dispose() => super.noSuchMethod(
        Invocation.method(
          #dispose,
          [],
        ),
        returnValueForMissingStub: null,
      );

  @override
  void notifyListeners() => super.noSuchMethod(
        Invocation.method(
          #notifyListeners,
          [],
        ),
        returnValueForMissingStub: null,
      );
}
