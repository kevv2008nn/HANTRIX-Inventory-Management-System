import 'package:flutter/material.dart';

import '../../data/recognition_service.dart';
import '../../models/recognition_setting.dart';

class RecognitionSettingsScreen extends StatefulWidget {
  const RecognitionSettingsScreen({super.key});

  @override
  State<RecognitionSettingsScreen> createState() =>
      _RecognitionSettingsScreenState();
}

class _RecognitionSettingsScreenState
    extends State<RecognitionSettingsScreen> {

  final RecognitionService service = RecognitionService();

  List<RecognitionSetting> settings = [];

  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadSettings();
  }

  Future<void> loadSettings() async {
    try {
      final result = await service.getSettings();

      setState(() {
        settings = result;
        loading = false;
      });
    } catch (e) {
      setState(() {
        loading = false;
      });

      debugPrint("Recognition settings error: $e");
    }
  }

  Future<void> changeSetting(
    int index,
    bool value,
  ) async {

    final method = settings[index].method;

    try {
      final updated = await service.updateSetting(
        method,
        value,
      );

      setState(() {
        settings[index] = updated;
      });
    } catch (e) {
      debugPrint("Update recognition error: $e");
    }
  }

  IconData getIcon(String method) {

    switch (method) {
      case "FACE":
        return Icons.face;

      case "ID_CARD":
        return Icons.badge;

      case "QR":
        return Icons.qr_code_scanner;

      case "RFID":
        return Icons.contactless;

      default:
        return Icons.security;
    }
  }

  String getName(String method) {

    switch (method) {
      case "FACE":
        return "Face Recognition";

      case "ID_CARD":
        return "ID Card";

      case "QR":
        return "QR Code";

      case "RFID":
        return "RFID";

      default:
        return method;
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Recognition Methods",
        ),
      ),

      body: loading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(20),
              itemCount: settings.length,

              itemBuilder: (context, index) {

                final setting = settings[index];

                return Card(
                  margin: const EdgeInsets.only(
                    bottom: 15,
                  ),

                  child: ListTile(

                    leading: Icon(
                      getIcon(setting.method),
                      size: 35,
                    ),

                    title: Text(
                      getName(setting.method),
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    subtitle: Text(
                      setting.enabled
                          ? "Enabled"
                          : "Disabled",
                    ),

                    trailing: Switch(
                      value: setting.enabled,

                      onChanged: (value) {
                        changeSetting(
                          index,
                          value,
                        );
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}