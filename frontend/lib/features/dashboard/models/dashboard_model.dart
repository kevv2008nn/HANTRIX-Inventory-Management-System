class DashboardModel {
  final int totalStudents;
  final int totalFaculty;
  final int totalComponents;
  final int studentsInside;
  final int borrowedComponents;
  final int notifications;
  final int lowStockComponents;
  final String? mostUsedComponent;

  DashboardModel({
    required this.totalStudents,
    required this.totalFaculty,
    required this.totalComponents,
    required this.studentsInside,
    required this.borrowedComponents,
    required this.notifications,
    required this.lowStockComponents,
    required this.mostUsedComponent,
  });

  factory DashboardModel.fromJson(
      Map<String, dynamic> json) {
    return DashboardModel(
      totalStudents:
          json["total_students"] ?? 0,

      totalFaculty:
          json["total_faculty"] ?? 0,

      totalComponents:
          json["total_components"] ?? 0,

      studentsInside:
          json["students_inside"] ?? 0,

      borrowedComponents:
          json["borrowed_components"] ?? 0,

      notifications:
          json["notifications"] ?? 0,

      lowStockComponents:
          json["low_stock_components"] ?? 0,

      mostUsedComponent:
          json["most_used_component"],
    );
  }
}