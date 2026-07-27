import 'package:flutter/material.dart';

class LiveCameraWidget extends StatelessWidget {
  const LiveCameraWidget({super.key});

  @override
  Widget build(BuildContext context) {

    return Container(

      height: 320,

      decoration: BoxDecoration(

        color: const Color(0xff1E293B),

        borderRadius:
            BorderRadius.circular(18),

      ),

      child: const Center(

        child: Column(

          mainAxisAlignment:
              MainAxisAlignment.center,

          children: [

            Icon(
              Icons.videocam,
              size: 70,
              color: Colors.white54,
            ),

            SizedBox(height: 20),

            Text(
              "Live Camera Feed",
              style: TextStyle(
                color: Colors.white,
                fontSize: 22,
              ),
            ),

            SizedBox(height: 10),

            Text(
              "Raspberry Pi Stream",
              style: TextStyle(
                color: Colors.white54,
              ),
            )

          ],
        ),
      ),
    );
  }
}