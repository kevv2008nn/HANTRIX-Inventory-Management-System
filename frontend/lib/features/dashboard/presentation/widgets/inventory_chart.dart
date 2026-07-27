import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class InventoryChart extends StatelessWidget {
  const InventoryChart({super.key});

  @override
  Widget build(BuildContext context) {

    return Container(

      height: 320,

      padding: const EdgeInsets.all(20),

      decoration: BoxDecoration(

        color: const Color(0xff1E293B),

        borderRadius:
            BorderRadius.circular(20),

      ),

      child: PieChart(

        PieChartData(

          sections: [

            PieChartSectionData(
              value: 45,
              color: Colors.cyan,
              title: "Available",
            ),

            PieChartSectionData(
              value: 25,
              color: Colors.orange,
              title: "Borrowed",
            ),

            PieChartSectionData(
              value: 10,
              color: Colors.red,
              title: "Low",
            ),

          ],

        ),

      ),

    );

  }

}