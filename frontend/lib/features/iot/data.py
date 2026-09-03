import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';

class IoTService {
  Future<List<dynamic>> getLatestReadings() async {
    try {
      final response = await ApiClient.dio.get(
        "/api/iot/latest",
      );

      print("IoT DATA:");
      print(response.data);

      return response.data;
    } catch (e) {
      print("IoT ERROR:");
      print(e);

      rethrow;
    }
  }
}