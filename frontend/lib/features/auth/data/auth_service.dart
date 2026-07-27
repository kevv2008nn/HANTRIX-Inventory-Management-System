import '../../../core/api/api_client.dart';

import '../models/login_request.dart';
import '../models/login_response.dart';

class AuthService {
  Future<LoginResponse> login(LoginRequest request) async {
    final response = await ApiClient.dio.post(
      "/auth/login",
      data: request.toJson(),
    );

    return LoginResponse.fromJson(response.data);
  }
}