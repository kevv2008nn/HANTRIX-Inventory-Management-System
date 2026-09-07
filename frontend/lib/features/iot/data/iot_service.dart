import 'package:dio/dio.dart';

class IoTService {
  final Dio dio = Dio();

  Future<List<dynamic>> getIoTData() async {
    final response = await dio.get(
      'http://192.168.76.43:8000/api/iot',
    );

    return response.data;
  }
}