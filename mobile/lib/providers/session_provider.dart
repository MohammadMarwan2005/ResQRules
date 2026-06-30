import 'package:flutter/foundation.dart';
import '../models/api_models.dart';
import '../services/api_service.dart';

class SessionProvider extends ChangeNotifier {
  final ApiService _api = ApiService();

  String? _sessionId;
  SessionResponse? _session;
  bool _loading = false;
  String? _error;

  String? get sessionId => _sessionId;
  SessionResponse? get session => _session;
  bool get loading => _loading;
  String? get error => _error;
  ScreenState? get screen => _session?.screen;
  bool get isAlive => _session?.alive ?? false;
  List<DangerPanelItem> get dangerPanel =>
      _session?.dangerPanel ?? const [];

  void _update({SessionResponse? session, bool loading = false, String? error}) {
    if (session != null) {
      _session = session;
      _sessionId = session.sessionId;
    }
    _loading = loading;
    _error = error;
    notifyListeners();
  }

  Future<void> startSession(String chartId) async {
    _update(loading: true, error: null);
    try {
      _update(session: await _api.createSession(chartId));
    } catch (e) {
      _update(loading: false, error: e.toString());
    }
  }

  Future<void> step(String input) async {
    if (_sessionId == null) return;
    _update(loading: true, error: null);
    try {
      _update(session: await _api.step(_sessionId!, input));
    } catch (e) {
      _update(loading: false, error: e.toString());
    }
  }

  Future<void> resetSession({String? chartId}) async {
    if (_sessionId == null) return;
    _update(loading: true, error: null);
    try {
      _update(session: await _api.reset(_sessionId!, chartId: chartId));
    } catch (e) {
      _update(loading: false, error: e.toString());
    }
  }

  Future<void> endSession() async {
    if (_sessionId != null) {
      await _api.deleteSession(_sessionId!);
    }
    _sessionId = null;
    _session = null;
    notifyListeners();
  }
}
