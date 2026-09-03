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
        title: const Text("Students"),
        centerTitle: true,
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),

        child: students.when(

          data: (list) {
            return StudentTable(
              students: list,
            );
          },

          loading: () {
            return const Center(
              child: CircularProgressIndicator(),
            );
          },

          error: (e, _) {
            return Center(
              child: Text(
                e.toString(),
                style: const TextStyle(
                  color: Colors.white,
                ),
              ),
            );
          },

        ),

      ),
    );
  }
}