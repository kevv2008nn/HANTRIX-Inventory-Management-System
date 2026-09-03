import 'dart:ui';
import 'package:flutter/material.dart';

class GlassCard extends StatelessWidget {
  final Widget child;

  const GlassCard({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(25),

      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 20,
          sigmaY: 20,
        ),

        child: Container(
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(.08),

            borderRadius:
                BorderRadius.circular(25),

            border: Border.all(
              color: Colors.white24,
            ),
          ),

          child: child,
        ),
      ),
    );
  }
}