class StudentModel {
  final int id;

  final String studentId;

  final String name;

  final String department;

  final int year;

  final String section;

  final String email;

  final String phone;

  final String imagePath;

  final bool faceRegistered;

  StudentModel({

    required this.id,

    required this.studentId,

    required this.name,

    required this.department,

    required this.year,

    required this.section,

    required this.email,

    required this.phone,

    required this.imagePath,

    required this.faceRegistered,

  });

  factory StudentModel.fromJson(

      Map<String,dynamic> json){

    return StudentModel(

      id: json["id"],

      studentId: json["student_id"],

      name: json["name"],

      department: json["department"],

      year: json["year"],

      section: json["section"],

      email: json["email"],

      phone: json["phone"],

      imagePath: json["image_path"],

      faceRegistered: json["face_registered"],

    );

  }

}