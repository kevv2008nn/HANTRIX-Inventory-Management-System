import '../models/student_model.dart';
import 'student_service.dart';

class StudentRepository {
  final StudentService service = StudentService();

  Future<List<StudentModel>> getStudents() async {
    return await service.getStudents();
  }

  Future<StudentModel> getStudent(String studentId) async {
    return await service.getStudent(studentId);
  }
}