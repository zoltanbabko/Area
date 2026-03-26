import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/oauth_webview.dart';

class ServicesScreen extends StatefulWidget {
  const ServicesScreen({super.key});

  @override
  State<ServicesScreen> createState() => _ServicesScreenState();
}

class _ServicesScreenState extends State<ServicesScreen> {
  Map<String, dynamic> services = {};
  bool isLoading = true;
  String? currentUserId;

  @override
  void initState() {
    super.initState();
    _fetchServices();
    _loadCurrentUser(); 
  }

  Future<void> _fetchServices() async {
    try {
      final data = await ApiService.get("/services");
      if(mounted) setState(() { services = data; isLoading = false; });
    } catch (e) {
      if(mounted) setState(() => isLoading = false);
    }
  }

  Future<void> _loadCurrentUser() async {
    final userId = await ApiService.getUserIdFromToken();
    
    if (mounted && userId != null) {
      setState(() {
        currentUserId = userId;
      });
    }
  }

  void _connect(String provider) {
    String url = "/auth/$provider/login";

    if (currentUserId != null) {
      url += "?user_id=$currentUserId";
    }
    Navigator.push(context, MaterialPageRoute(builder: (_) => OAuthWebView(
      url: url,
      onSuccess: (_) {
        _fetchServices();
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Connected!")));
      },
    )));
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Center(child: CircularProgressIndicator());

    return ListView(
      padding: const EdgeInsets.all(10),
      children: services.entries.map((e) {
        final name = e.key;
        final data = e.value;
        final isConnected = data['connected'] == true;
        
        return Card(
          child: ListTile(
            leading: Icon(
              isConnected ? Icons.check_circle : Icons.public,
              color: isConnected ? Colors.green : Colors.grey,
            ),
            title: Text(name.toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold)),
            trailing: isConnected 
              ? const Chip(label: Text("Active"), backgroundColor: Colors.greenAccent)
              : ElevatedButton(
                  onPressed: data['auth_provider'] != null ? () => _connect(data['auth_provider']) : null,
                  child: const Text("Connect"),
                ),
          ),
        );
      }).toList(),
    );
  }
}