import 'package:dio/dio.dart';

class IoTService {
  final Dio dio = Dio();

  Future<List<dynamic>> getIoTData() async {
    final response = await dio.get(
      'http://192.168.77.104:8000/api/iot',
    );

    return response.data;
  }
}