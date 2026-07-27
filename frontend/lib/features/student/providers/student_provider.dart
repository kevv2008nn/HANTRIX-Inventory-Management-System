import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/student_repository.dart';

import '../models/student_model.dart';

final studentProvider=

FutureProvider<List<StudentModel>>(

(ref){

return StudentRepository()

.getStudents();

}

);