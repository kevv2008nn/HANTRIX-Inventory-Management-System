import '../models/student_model.dart';

import 'student_service.dart';

class StudentRepository{

  final StudentService service=

      StudentService();

  Future<List<StudentModel>>

  getStudents(){

    return service.getStudents();

  }

}