import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme/app_theme.dart';
import 'routes/app_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(
    const ProviderScope(
      child: SmartLabOS(),
    ),
  );
}

class SmartLabOS extends StatelessWidget {
  const SmartLabOS({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,

      title: "SmartLab OS",

      theme: AppTheme.darkTheme,

      routerConfig: appRouter,
    );
  }
}