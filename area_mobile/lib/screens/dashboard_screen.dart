import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'edit_area_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<dynamic> areas = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchAreas();
  }

  Future<void> _fetchAreas() async {
    try {
      final data = await ApiService.get("/areas/");
      if (mounted) setState(() { areas = data; isLoading = false; });
    } catch (e) {
      if (mounted) setState(() => isLoading = false);
    }
  }

  Future<void> _toggleArea(int id, bool currentValue) async {
    setState(() {
      final index = areas.indexWhere((element) => element['id'] == id);
      if (index != -1) areas[index]['is_active'] = !currentValue;
    });

    try {
      await ApiService.patch("/areas/$id", {"is_active": !currentValue});
    } catch (e) {
      _fetchAreas();
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  Future<void> _deleteArea(int id) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text("Delete Automation?"),
        content: const Text("This action cannot be undone."),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text("Cancel")),
          TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text("Delete", style: TextStyle(color: Colors.red))),
        ],
      ),
    );

    if (confirm == true) {
      await ApiService.delete("/areas/$id");
      _fetchAreas();
    }
  }

  Color _getServiceColor(String serviceName) {
    if (serviceName.contains('google')) return Colors.redAccent;
    if (serviceName.contains('discord')) return Colors.indigoAccent;
    if (serviceName.contains('github')) return Colors.black87;
    if (serviceName.contains('spotify')) return Colors.green;
    if (serviceName.contains('timer')) return Colors.orange;
    return Colors.blueGrey;
  }

  String _formatName(String raw) {
    if (!raw.contains('.')) return raw;
    final parts = raw.split('.');
    String name = parts.length > 1 ? parts[1] : parts[0];
    return name.replaceAll('_', ' ').split(' ').map((s) => s.isNotEmpty ? '${s[0].toUpperCase()}${s.substring(1)}' : '').join(' ');
  }

  String _getServiceName(String raw) => raw.split('.')[0].toUpperCase();

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Center(child: CircularProgressIndicator());
    
    if (areas.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.auto_awesome_motion, size: 80, color: Colors.indigo.shade100),
            const SizedBox(height: 20),
            const Text("No Automation yet.", style: TextStyle(fontSize: 18, color: Colors.grey)),
            const SizedBox(height: 10),
            const Text("Create your first AREA to get started!", style: TextStyle(color: Colors.grey)),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _fetchAreas,
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: areas.length,
        separatorBuilder: (_, __) => const SizedBox(height: 16),
        itemBuilder: (ctx, i) {
          final area = areas[i];
          final bool isActive = area['is_active'] == true;
          final Color primaryColor = _getServiceColor(area['action']);

          return Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))
              ],
              border: Border.all(color: isActive ? primaryColor.withOpacity(0.3) : Colors.transparent, width: 1.5),
            ),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isActive ? primaryColor.withOpacity(0.1) : Colors.grey.shade50,
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 4)],
                        ),
                        child: Icon(isActive ? Icons.bolt : Icons.pause, color: isActive ? primaryColor : Colors.grey, size: 20),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          area['name'] ?? "Untitled Automation",
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: isActive ? Colors.black87 : Colors.grey),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      Switch(
                        value: isActive,
                        activeColor: primaryColor,
                        onChanged: (val) => _toggleArea(area['id'], isActive),
                      ),
                    ],
                  ),
                ),
                
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(_getServiceName(area['action']), style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.grey.shade600)),
                            const SizedBox(height: 4),
                            Text(_formatName(area['action']), style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                          ],
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        child: Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey.shade300),
                      ),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(_getServiceName(area['reaction']), style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.grey.shade600)),
                            const SizedBox(height: 4),
                            Text(_formatName(area['reaction']), style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14), textAlign: TextAlign.right),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    border: Border(top: BorderSide(color: Colors.grey.shade100)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      TextButton.icon(
                        onPressed: () async {
                          await Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => EditAreaScreen(areaId: area['id'])),
                          );
                          _fetchAreas();
                        },
                        icon: const Icon(Icons.edit, size: 18),
                        label: const Text("Edit"),
                        style: TextButton.styleFrom(foregroundColor: Colors.grey.shade700),
                      ),
                      const SizedBox(width: 8),
                      TextButton.icon(
                        onPressed: () => _deleteArea(area['id']),
                        icon: const Icon(Icons.delete, size: 18),
                        label: const Text("Delete"),
                        style: TextButton.styleFrom(foregroundColor: Colors.redAccent),
                      ),
                    ],
                  ),
                )
              ],
            ),
          );
        },
      ),
    );
  }
}