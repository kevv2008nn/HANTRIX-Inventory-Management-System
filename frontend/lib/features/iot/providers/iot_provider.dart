import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/iot_service.dart';

final iotServiceProvider = Provider<IoTService>((ref) {
  return IoTService();
});

final iotDataProvider = FutureProvider<List<dynamic>>((ref) async {
  final service = ref.read(iotServiceProvider);

  return await service.getIoTData();
});