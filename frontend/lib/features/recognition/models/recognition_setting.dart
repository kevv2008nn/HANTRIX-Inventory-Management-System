class RecognitionSetting {
  final String method;
  final bool enabled;

  RecognitionSetting({
    required this.method,
    required this.enabled,
  });

  factory RecognitionSetting.fromJson(Map<String, dynamic> json) {
    return RecognitionSetting(
      method: json["method"] ?? "",
      enabled: json["enabled"] ?? false,
    );
  }
}