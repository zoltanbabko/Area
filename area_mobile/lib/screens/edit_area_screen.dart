import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/dynamic_form.dart';

class EditAreaScreen extends StatefulWidget {
  final int areaId;
  const EditAreaScreen({super.key, required this.areaId});

  @override
  State<EditAreaScreen> createState() => _EditAreaScreenState();
}

class _EditAreaScreenState extends State<EditAreaScreen> {
  bool isLoading = true;
  Map<String, dynamic> services = {};
  
  final TextEditingController _nameCtrl = TextEditingController();
  
  String? selectedActionService;
  Map<String, dynamic>? selectedAction; 
  Map<String, dynamic> actionParamsValues = {}; 

  String? selectedReactionService;
  Map<String, dynamic>? selectedReaction; 
  Map<String, dynamic> reactionParamsValues = {}; 

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final servicesData = await ApiService.get("/services");
      final areaData = await ApiService.get("/areas/${widget.areaId}");

      if (mounted) {
        setState(() {
          services = servicesData;
          
          _nameCtrl.text = areaData['name'];

          final actionFull = areaData['action'] as String;
          final actionParts = actionFull.split('.');
          if (actionParts.length == 2) {
             selectedActionService = actionParts[0];
             final actionsList = services[selectedActionService]?['actions'] as List?;
             selectedAction = actionsList?.firstWhere((a) => a['name'] == actionParts[1], orElse: () => null);
             actionParamsValues = areaData['action_params'] ?? {};
          }

          final reactionFull = areaData['reaction'] as String;
          final reactionParts = reactionFull.split('.');
          if (reactionParts.length == 2) {
             selectedReactionService = reactionParts[0];
             final reactionsList = services[selectedReactionService]?['reactions'] as List?;
             selectedReaction = reactionsList?.firstWhere((r) => r['name'] == reactionParts[1], orElse: () => null);
             reactionParamsValues = areaData['reaction_params'] ?? {};
          }

          isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error loading data: $e")));
        Navigator.pop(context);
      }
    }
  }

  void _submit() async {
    if (_nameCtrl.text.isEmpty || selectedAction == null || selectedReaction == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Please fill all fields")));
      return;
    }

    final payload = {
      "name": _nameCtrl.text,
      "action": "$selectedActionService.${selectedAction!['name']}",
      "reaction": "$selectedReactionService.${selectedReaction!['name']}",
      "action_params": actionParamsValues,
      "reaction_params": reactionParamsValues,
    };

    try {
      await ApiService.patch("/areas/${widget.areaId}", payload);
      
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Updated Successfully!")));
      Navigator.pop(context);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Update failed: $e")));
      }
    }
  }

  Widget _buildDropdown<T>({
    required String label,
    required T? value,
    required List<DropdownMenuItem<T>> items,
    required ValueChanged<T?> onChanged,
  }) {
    return InputDecorator(
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<T>(
          value: value,
          isExpanded: true,
          items: items,
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, Color color) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 8),
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        border: Border(bottom: BorderSide(color: color, width: 2))
      ),
      child: Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    final actionServices = services.keys.where((k) => (services[k]['actions'] as List).isNotEmpty).toList();
    final reactionServices = services.keys.where((k) => (services[k]['reactions'] as List).isNotEmpty).toList();

    return Scaffold(
      appBar: AppBar(title: const Text("Edit Automation")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: _nameCtrl, 
              decoration: const InputDecoration(labelText: "Automation Name", border: OutlineInputBorder()),
            ),
            const SizedBox(height: 20),
            
            _buildSectionHeader("Trigger", Colors.blue),
            
            _buildDropdown<String>(
              label: "Service",
              value: selectedActionService,
              items: actionServices.map((s) => DropdownMenuItem(value: s, child: Text(s.toUpperCase()))).toList(),
              onChanged: (v) => setState(() { selectedActionService = v; selectedAction = null; actionParamsValues = {}; }),
            ),

            if (selectedActionService != null) ...[
               const SizedBox(height: 10),
               _buildDropdown<Map<String, dynamic>>(
                  label: "Event",
                  value: selectedAction,
                  items: (services[selectedActionService]['actions'] as List).map<DropdownMenuItem<Map<String, dynamic>>>((a) {
                    return DropdownMenuItem(value: a, child: Text(a['description'] ?? a['name']));
                  }).toList(),
                  onChanged: (v) => setState(() { selectedAction = v; actionParamsValues = {}; }),
               ),
               if (selectedAction != null && selectedAction!['args'] != null)
                 DynamicForm(
                   schema: selectedAction!['args'], 
                   values: actionParamsValues, 
                   onChange: (k, v) => setState(() => actionParamsValues[k] = v),
                   formContext: {'service': selectedActionService!, 'type': 'actions', 'name': selectedAction!['name']},
                 )
            ],

            const SizedBox(height: 30),

            _buildSectionHeader("Reaction", Colors.green),
            
            _buildDropdown<String>(
              label: "Service",
              value: selectedReactionService,
              items: reactionServices.map((s) => DropdownMenuItem(value: s, child: Text(s.toUpperCase()))).toList(),
              onChanged: (v) => setState(() { selectedReactionService = v; selectedReaction = null; reactionParamsValues = {}; }),
            ),

            if (selectedReactionService != null) ...[
               const SizedBox(height: 10),
               _buildDropdown<Map<String, dynamic>>(
                  label: "Action",
                  value: selectedReaction,
                  items: (services[selectedReactionService]['reactions'] as List).map<DropdownMenuItem<Map<String, dynamic>>>((r) {
                    return DropdownMenuItem(value: r, child: Text(r['description'] ?? r['name']));
                  }).toList(),
                  onChanged: (v) => setState(() { selectedReaction = v; reactionParamsValues = {}; }),
               ),
               if (selectedReaction != null && selectedReaction!['args'] != null)
                 DynamicForm(
                   schema: selectedReaction!['args'], 
                   values: reactionParamsValues, 
                   onChange: (k, v) => setState(() => reactionParamsValues[k] = v),
                   formContext: {'service': selectedReactionService!, 'type': 'reactions', 'name': selectedReaction!['name']},
                 )
            ],

            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo, foregroundColor: Colors.white),
                child: const Text("SAVE CHANGES"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}