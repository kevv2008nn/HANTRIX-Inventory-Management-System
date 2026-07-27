import 'package:flutter/material.dart';

import '../../models/student_model.dart';

class StudentTable extends StatelessWidget {
  final List<StudentModel> students;

  const StudentTable({
    super.key,
    required this.students,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 10,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: DataTable(

          headingRowColor:
              MaterialStateProperty.all(
            Colors.blueGrey.shade100,
          ),

          columns: const [

            DataColumn(
              label: Text("Photo"),
            ),

            DataColumn(
              label: Text("Student ID"),
            ),

            DataColumn(
              label: Text("Name"),
            ),

            DataColumn(
              label: Text("Department"),
            ),

            DataColumn(
              label: Text("Year"),
            ),

            DataColumn(
              label: Text("Section"),
            ),

            DataColumn(
              label: Text("Face"),
            ),

            DataColumn(
              label: Text("Action"),
            ),
          ],

          rows: students.map((student) {

            return DataRow(

              cells: [

                DataCell(

                  CircleAvatar(

                    radius: 22,

                    backgroundImage:
                        student.imagePath.isNotEmpty
                            ? NetworkImage(
                                student.imagePath,
                              )
                            : null,

                    child: student.imagePath.isEmpty
                        ? const Icon(Icons.person)
                        : null,

                  ),

                ),

                DataCell(
                  Text(student.studentId),
                ),

                DataCell(
                  Text(student.name),
                ),

                DataCell(
                  Text(student.department),
                ),

                DataCell(
                  Text(
                    student.year.toString(),
                  ),
                ),

                DataCell(
                  Text(student.section),
                ),

                DataCell(

                  Icon(

                    student.faceRegistered

                        ? Icons.verified

                        : Icons.cancel,

                    color:
                        student.faceRegistered
                            ? Colors.green
                            : Colors.red,

                  ),

                ),

                DataCell(

                  Row(

                    children: [

                      IconButton(

                        icon: const Icon(
                          Icons.visibility,
                          color: Colors.blue,
                        ),

                        onPressed: () {

                          ScaffoldMessenger.of(
                                  context)
                              .showSnackBar(

                            SnackBar(
                              content: Text(
                                "Open ${student.name}",
                              ),
                            ),

                          );

                        },

                      ),

                      IconButton(

                        icon: const Icon(
                          Icons.edit,
                          color: Colors.orange,
                        ),

                        onPressed: () {

                          ScaffoldMessenger.of(
                                  context)
                              .showSnackBar(

                            SnackBar(
                              content: Text(
                                "Edit ${student.name}",
                              ),
                            ),

                          );

                        },

                      ),

                      IconButton(

                        icon: const Icon(
                          Icons.delete,
                          color: Colors.red,
                        ),

                        onPressed: () {

                          showDialog(

                            context: context,

                            builder: (_) {

                              return AlertDialog(

                                title: const Text(
                                  "Delete Student",
                                ),

                                content: Text(
                                  "Delete ${student.name} ?",
                                ),

                                actions: [

                                  TextButton(

                                    onPressed: () {

                                      Navigator.pop(
                                          context);

                                    },

                                    child: const Text(
                                        "Cancel"),

                                  ),

                                  ElevatedButton(

                                    onPressed: () {

                                      Navigator.pop(
                                          context);

                                      ScaffoldMessenger
                                              .of(context)
                                          .showSnackBar(

                                        SnackBar(
                                          content: Text(
                                            "${student.name} deleted (Coming Soon)",
                                          ),
                                        ),

                                      );

                                    },

                                    child:
                                        const Text(
                                            "Delete"),

                                  ),

                                ],

                              );

                            },

                          );

                        },

                      ),

                    ],

                  ),

                ),

              ],

            );

          }).toList(),

        ),
      ),
    );
  }
}