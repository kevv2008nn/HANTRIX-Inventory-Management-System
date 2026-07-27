import '../models/login_request.dart';
import '../models/login_response.dart';

import 'auth_service.dart';

class AuthRepository {

  final AuthService service = AuthService();

  Future<LoginResponse> login(

      LoginRequest request

      ) {

    return service.login(request);

  }

}