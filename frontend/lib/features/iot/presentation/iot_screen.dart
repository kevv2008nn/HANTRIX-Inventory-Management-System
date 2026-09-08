import 'dart:async';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

import '../../../core/api/api_client.dart';

class IoTScreen extends StatefulWidget {
  const IoTScreen({super.key});

  @override
  State<IoTScreen> createState() => _IoTScreenState();
}

class _IoTScreenState extends State<IoTScreen> {
  final Dio dio = ApiClient.dio;

  Timer? timer;

  double temperature = 0.0;
  double humidity = 0.0;

  bool connected = false;
  bool loading = true;

  String lastUpdated = "--";

  @override
  void initState() {
    super.initState();

    fetchIoTData();

    // Automatically update every 3 seconds
    timer = Timer.periodic(
      const Duration(seconds: 3),
      (_) => fetchIoTData(),
    );
  }

  Future<void> fetchIoTData() async {
    try {
      final response = await dio.get(
        "/api/iot",
      );

      final List data = response.data;

      double? latestTemperature;
      double? latestHumidity;

      // Backend returns newest records first.
      // Find the FIRST/latest record for each metric.
      for (final item in data) {
        final metric = item["metric"];
        final value = double.tryParse(
          item["value"].toString(),
        );

        if (metric == "temperature" && latestTemperature == null) {
          latestTemperature = value;
        }

        if (metric == "humidity" && latestHumidity == null) {
          latestHumidity = value;
        }

        if (latestTemperature != null &&
            latestHumidity != null) {
          break;
        }
      }

      if (!mounted) return;

      setState(() {
        if (latestTemperature != null) {
          temperature = latestTemperature;
        }

        if (latestHumidity != null) {
          humidity = latestHumidity;
        }

        connected = true;
        loading = false;
        lastUpdated = TimeOfDay.now().format(context);
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        connected = false;
        loading = false;
      });

      debugPrint("IoT Error: $e");
    }
  }

  @override
  void dispose() {
    timer?.cancel();
    dio.close();

    super.dispose();
  }

  Widget sensorCard({
    required String title,
    required String value,
    required String unit,
    required IconData icon,
    required Color color,
  }) {
    return Card(
      elevation: 5,
      child: Padding(
        padding: const EdgeInsets.all(20),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [
            Icon(
              icon,
              size: 55,
              color: color,
            ),

            const SizedBox(height: 15),

            Text(
              title,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              "$value $unit",
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("IoT Monitoring"),
        centerTitle: true,

        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 15),

            child: Row(
              children: [
                Icon(
                  Icons.circle,
                  size: 13,
                  color: connected
                      ? Colors.green
                      : Colors.red,
                ),

                const SizedBox(width: 6),

                Text(
                  connected ? "LIVE" : "OFFLINE",
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),

        child: Column(
          children: [
            // CONNECTION STATUS
            Container(
              width: double.infinity,

              padding: const EdgeInsets.all(15),

              decoration: BoxDecoration(
                color: connected
                    ? Colors.green.withOpacity(0.12)
                    : Colors.red.withOpacity(0.12),

                borderRadius: BorderRadius.circular(12),
              ),

              child: Row(
                children: [
                  Icon(
                    connected
                        ? Icons.wifi
                        : Icons.wifi_off,

                    color: connected
                        ? Colors.green
                        : Colors.red,
                  ),

                  const SizedBox(width: 10),

                  Text(
                    connected
                        ? "IoT Backend Connected"
                        : "Unable to connect",

                    style: TextStyle(
                      fontWeight: FontWeight.bold,

                      color: connected
                          ? Colors.green
                          : Colors.red,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 25),

            // SENSOR CARDS
            if (loading)

              const Expanded(
                child: Center(
                  child: CircularProgressIndicator(),
                ),
              )

            else

              Expanded(
                child: GridView.count(
                  crossAxisCount: 2,

                  crossAxisSpacing: 15,
                  mainAxisSpacing: 15,

                  children: [
                    sensorCard(
                      title: "Temperature",
                      value: temperature
                          .toStringAsFixed(1),
                      unit: "°C",
                      icon: Icons.thermostat,
                      color: Colors.red,
                    ),

                    sensorCard(
                      title: "Humidity",
                      value: humidity
                          .toStringAsFixed(1),
                      unit: "%",
                      icon: Icons.water_drop,
                      color: Colors.blue,
                    ),

                    sensorCard(
                      title: "Backend",
                      value: connected
                          ? "ONLINE"
                          : "OFFLINE",
                      unit: "",
                      icon: Icons.cloud_done,
                      color: Colors.green,
                    ),

                    sensorCard(
                      title: "Refresh",
                      value: "3",
                      unit: "sec",
                      icon: Icons.sync,
                      color: Colors.orange,
                    ),
                  ],
                ),
              ),

            Text(
              "Last updated: $lastUpdated",
              style: const TextStyle(
                color: Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }
}