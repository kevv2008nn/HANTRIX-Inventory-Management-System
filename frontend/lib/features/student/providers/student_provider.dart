import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/student_repository.dart';
import '../models/student_model.dart';

final studentRepositoryProvider =
    Provider<StudentRepository>((ref) {
  return StudentRepository();
});

final studentProvider =
    FutureProvider<List<StudentModel>>((ref) async {
  final repo = ref.read(studentRepositoryProvider);
  return repo.getStudents();
});