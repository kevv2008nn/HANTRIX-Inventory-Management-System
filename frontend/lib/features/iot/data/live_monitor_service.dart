import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

class LiveMonitorService {
  WebSocketChannel? _channel;

  Stream<Map<String, dynamic>> connect() {
    _channel = WebSocketChannel.connect(
      Uri.parse(
        "ws://192.168.76.43:8000/ws",
      ),
    );

    return _channel!.stream.map((message) {
      print("LIVE DATA:");
      print(message);

      final data = jsonDecode(message);

      return Map<String, dynamic>.from(data);
    });
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
  }
}