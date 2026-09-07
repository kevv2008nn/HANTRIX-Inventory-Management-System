import 'package:flutter/material.dart';

import '../../../student/presentation/screens/student_list_screen.dart';
import '../../../recognition/presentation/screens/recognition_settings_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  Widget buildCard(
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Card(
      elevation: 5,
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 45,
              color: color,
            ),

            const SizedBox(height: 15),

            Text(
              value,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              title,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("SmartLab OS"),
        centerTitle: true,
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),

        child: Column(
          children: [

            // =========================
            // CAMERA
            // =========================

            Container(
              height: 250,
              width: double.infinity,

              decoration: BoxDecoration(
                color: Colors.black12,
                borderRadius: BorderRadius.circular(15),
              ),

              child: const Center(
                child: Text(
                  "📷 Raspberry Pi Live Camera\nComing Soon",
                  textAlign: TextAlign.center,

                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),

            const SizedBox(height: 25),

            // =========================
            // DASHBOARD CARDS
            // =========================

            Expanded(
              child: GridView.count(
                crossAxisCount: 2,

                crossAxisSpacing: 15,
                mainAxisSpacing: 15,

                children: [

                  // =========================
                  // STUDENTS PRESENT
                  // =========================

                  buildCard(
                    "Students Present",
                    "0",
                    Icons.people,
                    Colors.blue,
                  ),

                  // =========================
                  // EQUIPMENT
                  // =========================

                  buildCard(
                    "Equipment",
                    "0",
                    Icons.inventory,
                    Colors.green,
                  ),

                  // =========================
                  // BORROWED
                  // =========================

                  buildCard(
                    "Borrowed",
                    "0",
                    Icons.assignment_return,
                    Colors.orange,
                  ),

                  // =========================
                  // FACE RECOGNITIONS
                  // =========================

                  buildCard(
                    "Face Recognitions",
                    "0",
                    Icons.face,
                    Colors.red,
                  ),

                  // =========================
                  // STUDENTS
                  // =========================

                  GestureDetector(
                    onTap: () {

                      Navigator.push(
                        context,

                        MaterialPageRoute(
                          builder: (context) =>
                              const StudentListScreen(),
                        ),
                      );

                    },

                    child: buildCard(
                      "Students",
                      "View",
                      Icons.school,
                      Colors.indigo,
                    ),
                  ),

                  // =========================
                  // RECOGNITION SETTINGS
                  // =========================

                  GestureDetector(
                    onTap: () {

                      Navigator.push(
                        context,

                        MaterialPageRoute(
                          builder: (context) =>
                              const RecognitionSettingsScreen(),
                        ),
                      );

                    },

                    child: buildCard(
                      "Recognition",
                      "Settings",
                      Icons.security,
                      Colors.purple,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}