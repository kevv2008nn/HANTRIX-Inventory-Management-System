import 'package:flutter/material.dart';

import '../../data/student_service.dart';
import '../../models/student_model.dart';

class StudentListScreen extends StatefulWidget {
  const StudentListScreen({super.key});

  @override
  State<StudentListScreen> createState() => _StudentListScreenState();
}

class _StudentListScreenState extends State<StudentListScreen> {
  final StudentService studentService = StudentService();

  List<StudentModel> students = [];

  bool loading = true;
  String errorMessage = "";

  @override
  void initState() {
    super.initState();
    loadStudents();
  }

  Future<void> loadStudents() async {
    try {
      final result = await studentService.getStudents();

      if (!mounted) return;

      setState(() {
        students = result;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        loading = false;
        errorMessage = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Students"),
        centerTitle: true,
      ),
      body: loading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : errorMessage.isNotEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Text(
                      "Failed to load students\n\n$errorMessage",
                      textAlign: TextAlign.center,
                    ),
                  ),
                )
              : students.isEmpty
                  ? const Center(
                      child: Text(
                        "No students registered",
                        style: TextStyle(
                          fontSize: 18,
                        ),
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: students.length,
                      itemBuilder: (context, index) {
                        final student = students[index];

                        return Card(
                          margin: const EdgeInsets.only(
                            bottom: 12,
                          ),
                          child: ListTile(
                            leading: CircleAvatar(
                              child: Text(
                                student.name.isNotEmpty
                                    ? student.name[0].toUpperCase()
                                    : "?",
                              ),
                            ),
                            title: Text(
                              student.name,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            subtitle: Text(
                              "${student.department} | "
                              "Year ${student.year} | "
                              "Section ${student.section}",
                            ),
                            trailing: Text(
                              student.faceRegistered
                                  ? "FACE ✓"
                                  : "FACE ✗",
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: student.faceRegistered
                                    ? Colors.green
                                    : Colors.red,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
    );
  }
}