import 'package:flutter/material.dart';

import '../widgets/login_card.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  Color(0xff020617),
                  Color(0xff0f172a),
                  Color(0xff1e293b),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
          ),

          Positioned(
            top: -120,
            left: -100,
            child: Container(
              width: 260,
              height: 260,
              decoration: BoxDecoration(
                color: Colors.cyan.withOpacity(.18),
                shape: BoxShape.circle,
              ),
            ),
          ),

          Positioned(
            bottom: -120,
            right: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                color: Colors.blueAccent.withOpacity(.12),
                shape: BoxShape.circle,
              ),
            ),
          ),

          const Center(
            child: LoginCard(),
          ),
        ],
      ),
    );
  }
}