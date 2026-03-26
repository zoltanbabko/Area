import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static String baseUrl = "http://10.0.2.2:8080"; 

  static Future<void> setBaseUrl(String ip) async {
    final prefs = await SharedPreferences.getInstance();
    if (!ip.startsWith("http")) ip = "http://$ip";
    if (ip.endsWith("/")) ip = ip.substring(0, ip.length - 1);
    await prefs.setString("server_ip", ip);
    baseUrl = ip;
  }

  static Future<void> loadBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    baseUrl = prefs.getString("server_ip") ?? "http://10.0.2.2:8080";
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }

  static Future<void> setToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString("token", token);
  }
  
  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove("token");
  }

  static Future<String?> getUserIdFromToken() async {
    final token = await getToken();
    if (token == null) return null;
    try {
      final parts = token.split('.');
      if (parts.length != 3) return null;
      String payload = parts[1];
      switch (payload.length % 4) {
        case 0: break;
        case 2: payload += '=='; break;
        case 3: payload += '='; break;
        default: return null;
      }
      final String decoded = utf8.decode(base64Url.decode(payload));
      final Map<String, dynamic> json = jsonDecode(decoded);
      return json['user_id']?.toString() ?? json['sub']?.toString();
    } catch (e) {
      return null;
    }
  }

  static Future<dynamic> get(String endpoint) async {
    final token = await getToken();
    try {
      final response = await http.get(
        Uri.parse("$baseUrl$endpoint"),
        headers: {
          "Content-Type": "application/json",
          if (token != null) "Authorization": "Bearer $token",
        },
      ).timeout(const Duration(seconds: 10));
      return _handleResponse(response);
    } catch (e) {
      throw Exception("Erreur connexion: $e");
    }
  }

  static Future<dynamic> post(String endpoint, Map<String, dynamic> data) async {
    final token = await getToken();
    try {
      final isLogin = endpoint == "/auth/login";
      final response = await http.post(
        Uri.parse("$baseUrl$endpoint"),
        headers: {
          "Content-Type": isLogin ? "application/x-www-form-urlencoded" : "application/json",
          if (token != null) "Authorization": "Bearer $token",
        },
        body: isLogin ? data : jsonEncode(data),
      ).timeout(const Duration(seconds: 10));
      return _handleResponse(response);
    } catch (e) {
      throw Exception("Erreur connexion: $e");
    }
  }

  static Future<dynamic> patch(String endpoint, Map<String, dynamic> data) async {
    final token = await getToken();
    try {
      final response = await http.patch(
        Uri.parse("$baseUrl$endpoint"),
        headers: {
          "Content-Type": "application/json",
          if (token != null) "Authorization": "Bearer $token",
        },
        body: jsonEncode(data),
      ).timeout(const Duration(seconds: 10));
      return _handleResponse(response);
    } catch (e) {
      throw Exception("Erreur connexion: $e");
    }
  }

  static Future<dynamic> delete(String endpoint) async {
    final token = await getToken();
    try {
      final response = await http.delete(
        Uri.parse("$baseUrl$endpoint"),
        headers: {
          "Content-Type": "application/json",
          if (token != null) "Authorization": "Bearer $token",
        },
      ).timeout(const Duration(seconds: 10));
      return _handleResponse(response);
    } catch (e) {
      throw Exception("Erreur connexion: $e");
    }
  }

  static dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) return {};
      try {
        return jsonDecode(response.body);
      } catch (e) {
        return response.body;
      }
    } else {
      String msg = "Erreur ${response.statusCode}";
      try {
        final errJson = jsonDecode(response.body);
        if (errJson['detail'] != null) msg = errJson['detail'];
      } catch (_) {}
      throw Exception(msg);
    }
  }
}