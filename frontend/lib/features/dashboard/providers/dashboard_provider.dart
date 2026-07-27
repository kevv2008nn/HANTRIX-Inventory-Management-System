import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/dashboard_repository.dart';
import '../models/dashboard_model.dart';

final dashboardProvider =
    FutureProvider<DashboardModel>((ref) async {
  final repository = DashboardRepository();

  return repository.getDashboard();
});