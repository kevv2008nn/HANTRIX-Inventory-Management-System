import 'package:dio/dio.dart';
import '../../../core/api/api_client.dart';
import '../models/student_model.dart';
class StudentService {

  Future<List<StudentModel>> getStudents() async {

    final response = await ApiClient.dio.get(

      "/students/",

    );

    return (response.data as List)

        .map(

          (e)=>StudentModel.fromJson(e),

        )

        .toList();

  }

}