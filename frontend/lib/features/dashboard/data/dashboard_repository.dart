import '../../../core/network/api_client.dart';
import '../models/dashboard_model.dart';

class DashboardRepository {
  Future<DashboardModel> getDashboard() async {
    final response = await ApiClient.dio.get(
      "/analytics/dashboard",
    );

    return DashboardModel.fromJson(response.data);
  }
}