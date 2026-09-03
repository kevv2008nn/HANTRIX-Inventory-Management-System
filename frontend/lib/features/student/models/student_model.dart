class StudentModel {
  final String studentId;
  final String name;
  final String department;
  final int year;
  final String section;
  final String imagePath;
  final bool faceRegistered;

  StudentModel({
    required this.studentId,
    required this.name,
    required this.department,
    required this.year,
    required this.section,
    required this.imagePath,
    required this.faceRegistered,
  });

  factory StudentModel.fromJson(Map<String, dynamic> json) {
    return StudentModel(
      studentId: json["student_id"]?.toString() ?? "",
      name: json["name"]?.toString() ?? "",
      department: json["department"]?.toString() ?? "",
      year: json["year"] is int
          ? json["year"]
          : int.tryParse(json["year"]?.toString() ?? "0") ?? 0,
      section: json["section"]?.toString() ?? "",
      imagePath: json["photo"]?.toString() ?? "",
      faceRegistered: json["face_registered"] == true,
    );
  }
}