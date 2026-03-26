import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'home_screen.dart';
import 'register_screen.dart';
import '../widgets/oauth_webview.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _usernameCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  final _ipCtrl = TextEditingController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _ipCtrl.text = ApiService.baseUrl;
  }

  void _login() async {
    setState(() => _isLoading = true);
    try {
      final res = await ApiService.post("/auth/login", {
        "username": _usernameCtrl.text.trim(),
        "password": _passCtrl.text.trim(),
      });
      if (res['access_token'] != null) {
        await ApiService.setToken(res['access_token']);
        if (mounted) Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen()));
      }
    } catch (e) {
      if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    } finally {
      if(mounted) setState(() => _isLoading = false);
    }
  }

  void _loginWithGoogle() {
    Navigator.push(context, MaterialPageRoute(builder: (_) => OAuthWebView(
      url: "/auth/google/login",
      onSuccess: (token) async {
        await ApiService.setToken(token);
        if (mounted) Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen()));
      },
    )));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AREA Login"),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings), 
            onPressed: () => showDialog(context: context, builder: (_) => AlertDialog(
              title: const Text("Server IP"),
              content: TextField(controller: _ipCtrl, decoration: const InputDecoration(hintText: "http://10.0.2.2:8080")),
              actions: [
                TextButton(onPressed: (){ ApiService.setBaseUrl(_ipCtrl.text); Navigator.pop(context); }, child: const Text("Save"))
              ],
            ))
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.hub, size: 80, color: Colors.indigo),
            const SizedBox(height: 20),
            TextField(controller: _usernameCtrl, decoration: const InputDecoration(labelText: "Username", border: OutlineInputBorder())),
            const SizedBox(height: 10),
            TextField(controller: _passCtrl, obscureText: true, decoration: const InputDecoration(labelText: "Password", border: OutlineInputBorder())),
            const SizedBox(height: 20),
            _isLoading ? const CircularProgressIndicator() : SizedBox(
              width: double.infinity,
              child: ElevatedButton(onPressed: _login, child: const Text("Login")),
            ),
            const SizedBox(height: 10),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                icon: const Icon(Icons.login),
                label: const Text("Sign in with Google"),
                onPressed: _loginWithGoogle,
              ),
            ),
            TextButton(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RegisterScreen())), 
              child: const Text("Create Account")
            )
          ],
        ),
      ),
    );
  }
}