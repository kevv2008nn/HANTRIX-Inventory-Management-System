import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  Widget buildItem(
    BuildContext context,
    IconData icon,
    String title,
    String route,
  ) {
    return ListTile(
      leading: Icon(icon, color: Colors.white70),
      title: Text(
        title,
        style: const TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.w500,
        ),
      ),
      onTap: () => context.go(route),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      hoverColor: Colors.blue.withOpacity(.2),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 240,
      color: const Color(0xff111827),
      child: Column(
        children: [
          const SizedBox(height: 40),

          const Icon(
            Icons.memory,
            size: 70,
            color: Colors.cyanAccent,
          ),

          const SizedBox(height: 15),

          const Text(
            "SmartLab OS",
            style: TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),

          const Divider(
            color: Colors.white24,
            height: 40,
          ),

          buildItem(
            context,
            Icons.dashboard,
            "Dashboard",
            "/dashboard",
          ),

          buildItem(
            context,
            Icons.people,
            "Students",
            "/students",
          ),

          buildItem(
            context,
            Icons.inventory,
            "Inventory",
            "/inventory",
          ),

          buildItem(
            context,
            Icons.analytics,
            "Analytics",
            "/analytics",
          ),

          buildItem(
            context,
            Icons.camera_alt,
            "Camera",
            "/camera",
          ),

          const Spacer(),

          const Divider(color: Colors.white24),

          buildItem(
            context,
            Icons.logout,
            "Logout",
            "/login",
          ),

          const SizedBox(height: 20),
        ],
      ),
    );
  }
}