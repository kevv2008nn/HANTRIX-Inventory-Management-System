import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';
import '../models/recognition_setting.dart';

class RecognitionService {

  Future<List<RecognitionSetting>> getSettings() async {

    final Response response = await ApiClient.dio.get(
      "/api/recognition/settings",
    );

    final List<dynamic> data = response.data;

    return data
        .map(
          (item) => RecognitionSetting.fromJson(
            item,
          ),
        )
        .toList();
  }


  Future<RecognitionSetting> updateSetting(
    String method,
    bool enabled,
  ) async {

    final Response response = await ApiClient.dio.put(
      "/api/recognition/settings/$method",
      data: {
        "enabled": enabled,
      },
    );

    return RecognitionSetting.fromJson(
      response.data,
    );
  }
}
