import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';
import '../models/login_request.dart';
import '../models/login_response.dart';

class AuthService {
  Future<LoginResponse> login(LoginRequest request) async {

    print("Trying Login...");
    print(request.email);
    print(request.password);

    final Response response = await ApiClient.dio.post(
      "/auth/login",
      data: request.toJson(),
    );

    print(response.data);

    return LoginResponse.fromJson(response.data);
  }
}