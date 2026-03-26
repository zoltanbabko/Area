import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class OAuthWebView extends StatefulWidget {
  final String url;
  final Function(String token) onSuccess;

  const OAuthWebView({super.key, required this.url, required this.onSuccess});

  @override
  State<OAuthWebView> createState() => _OAuthWebViewState();
}

class _OAuthWebViewState extends State<OAuthWebView> {
  late final WebViewController _controller;
  bool _isHandling = false;

  @override
  void initState() {
    super.initState();
    WebViewCookieManager().clearCookies();

    final fullUrl = widget.url.startsWith("http") 
        ? widget.url 
        : "${ApiService.baseUrl}${widget.url}";

    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setUserAgent("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36")
      ..setNavigationDelegate(
        NavigationDelegate(
          onNavigationRequest: (NavigationRequest request) {
            if (request.url.contains('token=')) {
              _handleTokenUrl(request.url);
              return NavigationDecision.prevent;
            }
            
            if (request.url.contains('/callback') && request.url.contains('code=')) {
              _handleManualExchange(request.url);
              return NavigationDecision.prevent;
            }

            return NavigationDecision.navigate;
          },
          onWebResourceError: (error) {
            debugPrint("Erreur WebView : ${error.description}");
          },
        ),
      )
      ..loadRequest(Uri.parse(fullUrl));
  }

  void _handleTokenUrl(String url) {
    if (_isHandling) return;
    final uri = Uri.parse(url);
    final token = uri.queryParameters['token'];
    if (token != null) {
      _isHandling = true;
      widget.onSuccess(token);
      Navigator.pop(context);
    }
  }

  Future<void> _handleManualExchange(String callbackUrl) async {
    if (_isHandling) return;
    _isHandling = true;

    try {
      final uri = Uri.parse(callbackUrl);
      final pathAndQuery = "${uri.path}?${uri.query}";
      
      final targetUrl = "${ApiService.baseUrl}$pathAndQuery";
    
      final client = http.Client();
      final request = http.Request('GET', Uri.parse(targetUrl))
        ..followRedirects = false;
        
      final response = await client.send(request);
      
      final location = response.headers['location'];
      
      if (location != null && location.contains('token=')) {
        final token = Uri.parse(location).queryParameters['token'];
        if (token != null && mounted) {
          widget.onSuccess(token);
          Navigator.pop(context);
          return;
        }
      }
    } catch (e) {
      debugPrint("Error manual switch : $e");
      if (mounted) {
        setState(() => _isHandling = false);
        _controller.loadRequest(Uri.parse(callbackUrl)); 
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Logging in...")),
      body: Center(child: WebViewWidget(controller: _controller)),
    );
  }
}