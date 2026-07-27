import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class AttendanceChart extends StatelessWidget {
  const AttendanceChart({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 320,
      padding: const EdgeInsets.all(20),

      decoration: BoxDecoration(
        color: const Color(0xff1E293B),
        borderRadius: BorderRadius.circular(20),
      ),

      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [

          const Text(
            "Weekly Attendance",
            style: TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 25),

          Expanded(
            child: LineChart(
              LineChartData(

                gridData: FlGridData(show: true),

                borderData: FlBorderData(show: false),

                titlesData: FlTitlesData(show: false),

                lineBarsData: [

                  LineChartBarData(

                    isCurved: true,

                    color: Colors.cyan,

                    barWidth: 5,

                    spots: const [

                      FlSpot(0,4),
                      FlSpot(1,5),
                      FlSpot(2,7),
                      FlSpot(3,8),
                      FlSpot(4,6),
                      FlSpot(5,9),
                      FlSpot(6,11),

                    ],

                  )

                ],

              ),
            ),
          ),
        ],
      ),
    );
  }
}