import 'package:flutter/material.dart';
import '../../models/dashboard_model.dart';
import 'dashboard_card.dart';

class StatisticsGrid extends StatelessWidget {
  final DashboardModel dashboard;

  const StatisticsGrid({
    super.key,
    required this.dashboard,
  });

  @override
  Widget build(BuildContext context) {
    return GridView.count(
      shrinkWrap: true,
      physics:
          const NeverScrollableScrollPhysics(),
      crossAxisCount: 4,
      crossAxisSpacing: 18,
      mainAxisSpacing: 18,
      childAspectRatio: 2.1,

      children: [

        DashboardCard(
          title: "Students",
          value:
              dashboard.totalStudents.toString(),
          icon: Icons.people,
          color: Colors.cyan,
        ),

        DashboardCard(
          title: "Faculty",
          value:
              dashboard.totalFaculty.toString(),
          icon: Icons.school,
          color: Colors.green,
        ),

        DashboardCard(
          title: "Components",
          value: dashboard.totalComponents
              .toString(),
          icon: Icons.inventory,
          color: Colors.orange,
        ),

        DashboardCard(
          title: "Inside Lab",
          value:
              dashboard.studentsInside.toString(),
          icon: Icons.login,
          color: Colors.purple,
        ),

        DashboardCard(
          title: "Borrowed",
          value: dashboard
              .borrowedComponents
              .toString(),
          icon: Icons.assignment,
          color: Colors.redAccent,
        ),

        DashboardCard(
          title: "Notifications",
          value: dashboard.notifications
              .toString(),
          icon: Icons.notifications,
          color: Colors.amber,
        ),

        DashboardCard(
          title: "Low Stock",
          value: dashboard
              .lowStockComponents
              .toString(),
          icon: Icons.warning,
          color: Colors.deepOrange,
        ),

        DashboardCard(
          title: "Most Used",
          value:
              dashboard.mostUsedComponent ??
                  "-",
          icon: Icons.star,
          color: Colors.lightBlue,
        ),
      ],
    );
  }
}