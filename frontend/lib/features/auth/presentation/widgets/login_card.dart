import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../providers/auth_provider.dart';

class LoginCard extends ConsumerStatefulWidget {
  const LoginCard({super.key});

  @override
  ConsumerState<LoginCard> createState() => _LoginCardState();
}

class _LoginCardState extends ConsumerState<LoginCard> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  bool remember = false;

  @override
  Widget build(BuildContext context) {
    final loading = ref.watch(authProvider);

    return ClipRRect(
      borderRadius: BorderRadius.circular(25),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 15,
          sigmaY: 15,
        ),
        child: Container(
          width: 420,
          padding: const EdgeInsets.all(30),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(.08),
            borderRadius: BorderRadius.circular(25),
            border: Border.all(color: Colors.white24),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.memory,
                size: 70,
                color: Colors.cyanAccent,
              ),

              const SizedBox(height: 15),

              const Text(
                "SmartLab OS",
                style: TextStyle(
                  fontSize: 32,
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 5),

              const Text(
                "AI Powered Laboratory",
                style: TextStyle(
                  color: Colors.white70,
                ),
              ),

              const SizedBox(height: 30),

              TextField(
                controller: emailController,
                decoration: const InputDecoration(
                  labelText: "Email",
                ),
              ),

              const SizedBox(height: 20),

              TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: "Password",
                ),
              ),

              const SizedBox(height: 15),

              Row(
                children: [
                  Checkbox(
                    value: remember,
                    onChanged: (v) {
                      setState(() {
                        remember = v ?? false;
                      });
                    },
                  ),
                  const Text("Remember Me"),
                ],
              ),

              const SizedBox(height: 20),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: loading
                      ? null
                      : () async {
                          print("================================");
                          print("BUTTON PRESSED");
                          print("Email : ${emailController.text}");
                          print("Password : ${passwordController.text}");
                          print("================================");

                          final error = await ref
                              .read(authProvider.notifier)
                              .login(
                                emailController.text,
                                passwordController.text,
                              );

                          print("Returned Error : $error");

                          if (!mounted) return;

                          if (error == null) {
                            print("GO TO DASHBOARD");
                            context.go("/dashboard");
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(error),
                              ),
                            );
                          }
                        },
                  child: loading
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Text(
                          "LOGIN",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}