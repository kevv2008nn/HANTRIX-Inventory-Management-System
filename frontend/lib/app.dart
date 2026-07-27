import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme/app_theme.dart';
import 'routes/app_router.dart';

class SmartLabApp extends ConsumerWidget {
  const SmartLabApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,
      title: "SmartLab OS",
      theme: AppTheme.darkTheme,
      routerConfig: appRouter,
    );
  }
}