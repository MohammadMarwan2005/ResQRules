import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/api_models.dart';

class ApiException implements Exception {
  final int statusCode;
  final String message;
  const ApiException(this.statusCode, this.message);

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiService {
  final _client = http.Client();

  Map<String, String> get _headers => {'Content-Type': 'application/json'};

  void _check(http.Response r) {
    if (r.statusCode >= 400) {
      final body = jsonDecode(r.body);
      throw ApiException(r.statusCode, body['detail']?.toString() ?? r.body);
    }
  }

  Future<List<ChartInfo>> getCharts() async {
    final r = await _client.get(Uri.parse('$kBaseUrl/charts'));
    _check(r);
    return (jsonDecode(r.body) as List)
        .map((c) => ChartInfo.fromJson(c))
        .toList();
  }

  Future<SessionResponse> createSession(String chartId) async {
    final r = await _client.post(
      Uri.parse('$kBaseUrl/sessions'),
      headers: _headers,
      body: jsonEncode({'chart_id': chartId}),
    );
    _check(r);
    return SessionResponse.fromJson(jsonDecode(r.body));
  }

  Future<SessionResponse> getSession(String sessionId) async {
    final r =
        await _client.get(Uri.parse('$kBaseUrl/sessions/$sessionId'));
    _check(r);
    return SessionResponse.fromJson(jsonDecode(r.body));
  }

  Future<SessionResponse> step(String sessionId, String input) async {
    final r = await _client.post(
      Uri.parse('$kBaseUrl/sessions/$sessionId/step'),
      headers: _headers,
      body: jsonEncode({'input': input}),
    );
    _check(r);
    return SessionResponse.fromJson(jsonDecode(r.body));
  }

  Future<SessionResponse> reset(String sessionId, {String? chartId}) async {
    final r = await _client.post(
      Uri.parse('$kBaseUrl/sessions/$sessionId/reset'),
      headers: _headers,
      body: jsonEncode({'chart_id': chartId}),
    );
    _check(r);
    return SessionResponse.fromJson(jsonDecode(r.body));
  }

  Future<void> deleteSession(String sessionId) async {
    await _client
        .delete(Uri.parse('$kBaseUrl/sessions/$sessionId'))
        .catchError((_) {});
  }

  void dispose() => _client.close();
}
