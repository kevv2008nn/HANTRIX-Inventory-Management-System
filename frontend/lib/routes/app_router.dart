import 'package:go_router/go_router.dart';

import '../features/auth/presentation/screens/login_screen.dart';
import '../features/dashboard/presentation/screens/dashboard_screen.dart';
import '../features/splash/presentation/screens/splash_screen.dart';
import '../features/student/presentation/screens/student_screen.dart';
final appRouter = GoRouter(
  initialLocation: "/",

  routes: [

    GoRoute(
      path: "/",
      builder: (context, state) => const SplashScreen(),
    ),

    GoRoute(
      path: "/login",
      builder: (context, state) => const LoginScreen(),
    ),

    GoRoute(
      path: "/dashboard",
      builder: (context, state) => const DashboardScreen(),
    ),
    GoRoute(
      path: "/students",
      builder: (context, state) => const StudentScreen(),
    ),

  ],
);