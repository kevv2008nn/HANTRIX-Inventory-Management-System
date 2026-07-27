import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../widgets/quick_action_card.dart';
import '../widgets/live_camera_widget.dart';
import '../widgets/notification_panel.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff0f172a),

      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text("SmartLab OS Dashboard"),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),

        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,

          children: [

            const SizedBox(height: 20),

            const Text(
              "Quick Actions",
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 20),

            SizedBox(
              height: 170,

              child: ListView(

                scrollDirection: Axis.horizontal,

                children: [

                  QuickActionCard(

                    icon: Icons.people,

                    title: "Students",

                    color: Colors.cyan,

                    onTap: () {

                      context.go("/students");

                    },

                  ),

                  const SizedBox(width: 20),

                  QuickActionCard(

                    icon: Icons.inventory,

                    title: "Inventory",

                    color: Colors.orange,

                    onTap: () {

                      context.go("/inventory");

                    },

                  ),

                  const SizedBox(width: 20),

                  QuickActionCard(

                    icon: Icons.analytics,

                    title: "Analytics",

                    color: Colors.green,

                    onTap: () {

                      context.go("/analytics");

                    },

                  ),

                  const SizedBox(width: 20),

                  QuickActionCard(

                    icon: Icons.camera_alt,

                    title: "Camera",

                    color: Colors.purple,

                    onTap: () {

                      context.go("/camera");

                    },

                  ),

                ],

              ),

            ),

            const SizedBox(height: 30),

            const LiveCameraWidget(),

            const SizedBox(height: 30),

            const NotificationPanel(),

          ],

        ),

      ),

    );
  }
}