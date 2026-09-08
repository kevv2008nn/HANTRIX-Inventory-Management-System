import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';

class IoTService {
  final Dio dio = ApiClient.dio;

  Future<List<dynamic>> getIoTData() async {
    final response = await dio.get(
      '/api/iot',
    );

    return response.data;
  }
}