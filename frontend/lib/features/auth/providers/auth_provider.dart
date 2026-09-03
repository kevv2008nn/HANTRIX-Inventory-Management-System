import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:state_notifier/state_notifier.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data/auth_repository.dart';
import '../models/login_request.dart';

final authProvider =
    StateNotifierProvider<AuthNotifier, bool>(
  (ref) => AuthNotifier(),
);

class AuthNotifier extends StateNotifier<bool> {
  AuthNotifier() : super(false);

  final AuthRepository repository = AuthRepository();

  Future<String?> login(
    String email,
    String password,
  ) async {
    try {
      print("================================");
      print("LOGIN STARTED");
      print("Email : $email");
      print("Password : $password");
      print("================================");

      state = true;

      final response = await repository.login(
        LoginRequest(
          email: email.trim(),
          password: password.trim(),
        ),
      );

      print("================================");
      print("LOGIN SUCCESS");
      print(response.accessToken);
      print("================================");

      final prefs =
          await SharedPreferences.getInstance();

      await prefs.setString(
        "token",
        response.accessToken,
      );

      state = false;

      return null;
    } catch (e, s) {
      state = false;

      print("================================");
      print("LOGIN FAILED");
      print(e);
      print(s);
      print("================================");

      return e.toString();
    }
  }
}