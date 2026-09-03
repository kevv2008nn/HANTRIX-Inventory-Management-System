import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';
import '../models/student_model.dart';

class StudentService {
  Future<List<StudentModel>> getStudents() async {
    final Response response = await ApiClient.dio.get(
      "/api/students/",
    );

    final List<dynamic> data = response.data;

    return data
        .map(
          (json) => StudentModel.fromJson(
            json as Map<String, dynamic>,
          ),
        )
        .toList();
  }

  Future<StudentModel> getStudent(String studentId) async {
    final Response response = await ApiClient.dio.get(
      "/api/students/$studentId",
    );

    return StudentModel.fromJson(
      response.data as Map<String, dynamic>,
    );
  }
}