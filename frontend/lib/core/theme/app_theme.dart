import 'package:flutter/material.dart';

class AppTheme {

  static ThemeData darkTheme = ThemeData(

    brightness: Brightness.dark,

    scaffoldBackgroundColor: Colors.black,

    useMaterial3: true,

    colorSchemeSeed: Colors.cyan,

    inputDecorationTheme: InputDecorationTheme(

      filled: true,

      fillColor: Colors.white10,

      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
      ),

    ),

    elevatedButtonTheme: ElevatedButtonThemeData(

      style: ElevatedButton.styleFrom(

        minimumSize: const Size(double.infinity, 50),

        backgroundColor: Colors.cyan,

        foregroundColor: Colors.black,

        shape: RoundedRectangleBorder(

          borderRadius: BorderRadius.circular(15),

        ),

      ),

    ),

  );

}