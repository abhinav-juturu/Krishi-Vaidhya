import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart'; // Add http_parser to pubspec if missing, or use string content type

class ApiService {
  static String get baseUrl {
    if (Platform.isAndroid) {
      return "http://10.0.2.2:5000/api";
    } else {
      return "http://127.0.0.1:5000/api";
    }
  }

  // --- AUTH ---
  static Future<Map<String, dynamic>?> login(String phone, String name, String language, List<String> crops) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/users/login'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "phone": phone,
          "name": name,
          "language": language,
          "crops": crops,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Login failed: ${response.statusCode}");
        return null;
      }
    } catch (e) {
      print("Login error: $e");
      return null;
    }
  }

  // --- DIAGNOSIS ---
  static Future<Map<String, dynamic>?> uploadImage(File imageFile, String userId, double lat, double lng) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/diagnosis'));
      
      request.fields['userId'] = userId;
      request.fields['lat'] = lat.toString();
      request.fields['lng'] = lng.toString();
      
      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          imageFile.path,
        ),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Upload failed: ${response.statusCode} - ${response.body}");
        return null; // Handle error appropriately in UI
      }
    } catch (e) {
      print("Upload error: $e");
      return null;
    }
  }

  // --- CALENDAR ---
  static Future<Map<String, dynamic>?> generateCalendar(String userId, String crop, String sowingDate, double lat, double lng) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/calendar/generate'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "userId": userId,
          "crop": crop,
          "sowingDate": sowingDate,
          "lat": lat,
          "lng": lng,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print("Calendar generation failed: ${response.body}");
        return null;
      }
    } catch (e) {
      print("Calendar error: $e");
      return null;
    }
  }
}
