import 'package:flutter/material.dart';

class NotificationPanel extends StatelessWidget {
  const NotificationPanel({super.key});

  @override
  Widget build(BuildContext context) {

    return Container(

      padding: const EdgeInsets.all(18),

      decoration: BoxDecoration(

        color: const Color(0xff1E293B),

        borderRadius:
            BorderRadius.circular(18),

      ),

      child: const Column(

        crossAxisAlignment:
            CrossAxisAlignment.start,

        children: [

          Text(
            "Recent Notifications",
            style: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),

          SizedBox(height: 20),

          ListTile(
            leading: Icon(
              Icons.notifications,
              color: Colors.orange,
            ),
            title: Text(
              "Low Stock Alert",
              style: TextStyle(
                  color: Colors.white),
            ),
          ),

          ListTile(
            leading: Icon(
              Icons.people,
              color: Colors.green,
            ),
            title: Text(
              "Student Checked In",
              style: TextStyle(
                  color: Colors.white),
            ),
          ),

          ListTile(
            leading: Icon(
              Icons.inventory,
              color: Colors.cyan,
            ),
            title: Text(
              "Component Returned",
              style: TextStyle(
                  color: Colors.white),
            ),
          )

        ],
      ),
    );
  }
}