import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/student_provider.dart';
import '../widgets/student_table.dart';

class StudentScreen extends ConsumerWidget {
  const StudentScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final students = ref.watch(studentProvider);

    return Scaffold(
      backgroundColor: const Color(0xff0f172a),

      appBar: AppBar(
        title: const Text("Student Management"),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),

      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        icon: const Icon(Icons.add),
        label: const Text("Add Student"),
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),

        child: students.when(

          loading: () =>
              const Center(
                child: CircularProgressIndicator(),
              ),

          error: (e, _) =>
              Center(
                child: Text(
                  e.toString(),
                  style: const TextStyle(
                    color: Colors.white,
                  ),
                ),
              ),

          data: (data) {

            return Column(

              crossAxisAlignment:
                  CrossAxisAlignment.start,

              children: [

                const Text(
                  "Students",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: 20),

                TextField(

                  decoration: InputDecoration(

                    filled: true,

                    fillColor: Colors.white,

                    prefixIcon:
                        const Icon(Icons.search),

                    hintText:
                        "Search Student",

                    border:
                        OutlineInputBorder(
                      borderRadius:
                          BorderRadius.circular(
                              15),
                    ),
                  ),
                ),

                const SizedBox(height: 20),

                Expanded(

                  child:
                      StudentTable(
                    students: data,
                  ),

                ),

              ],
            );
          },
        ),
      ),
    );
  }
}