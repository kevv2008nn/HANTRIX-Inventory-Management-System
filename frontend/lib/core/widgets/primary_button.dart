import 'package:flutter/material.dart';

import '../theme/app_colors.dart';

class PrimaryButton extends StatelessWidget {
  final String title;

  final VoidCallback? onPressed;

  final bool loading;

  const PrimaryButton({
    super.key,
    required this.title,
    required this.onPressed,
    this.loading = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 55,

      width: double.infinity,

      child: ElevatedButton(
        onPressed: loading
            ? null
            : onPressed,

        style: ElevatedButton.styleFrom(
          backgroundColor:
              AppColors.primary,

          foregroundColor: Colors.black,

          shape: RoundedRectangleBorder(
            borderRadius:
                BorderRadius.circular(15),
          ),
        ),

        child: loading
            ? const CircularProgressIndicator()
            : Text(
                title,
                style: const TextStyle(
                  fontWeight:
                      FontWeight.bold,
                  fontSize: 18,
                ),
              ),
      ),
    );
  }
}