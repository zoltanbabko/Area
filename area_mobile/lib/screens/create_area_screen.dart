import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/dynamic_form.dart'; 

class CreateAreaScreen extends StatefulWidget {
  const CreateAreaScreen({super.key});

  @override
  State<CreateAreaScreen> createState() => _CreateAreaScreenState();
}

class _CreateAreaScreenState extends State<CreateAreaScreen> {
  Map<String, dynamic> services = {};
  bool isLoading = true;

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
    _fetchServices();
  }

  Future<void> _fetchServices() async {
    try {
      final data = await ApiService.get("/services");
      if (mounted) setState(() { services = data; isLoading = false; });
    } catch (e) {
      if (mounted) setState(() => isLoading = false);
    }
  }

  void _onActionParamChange(String key, dynamic value) {
    setState(() => actionParamsValues[key] = value);
  }

  void _onReactionParamChange(String key, dynamic value) {
    setState(() => reactionParamsValues[key] = value);
  }

  void _submit() async {
    if (_nameCtrl.text.isEmpty || selectedAction == null || selectedReaction == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Please fill name, action and reaction")));
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
      await ApiService.post("/areas/", payload);
      
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("AREA Created Successfully! 🚀"), backgroundColor: Colors.green));
      
      _nameCtrl.clear();
      setState(() {
        selectedAction = null; 
        selectedReaction = null;
        actionParamsValues = {};
        reactionParamsValues = {};
        selectedActionService = null;
        selectedReactionService = null;
      });

    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e"), backgroundColor: Colors.red));
      }
    }
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

  @override
  Widget build(BuildContext context) {
    if (isLoading) return const Center(child: CircularProgressIndicator());

    final actionServices = services.keys.where((k) => (services[k]['actions'] as List).isNotEmpty).toList();
    final reactionServices = services.keys.where((k) => (services[k]['reactions'] as List).isNotEmpty).toList();

    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(
              child: Text("Create Automation", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.indigo)),
            ),
            const SizedBox(height: 20),
            
            TextField(
              controller: _nameCtrl, 
              decoration: const InputDecoration(labelText: "Automation Name", border: OutlineInputBorder(), prefixIcon: Icon(Icons.edit)),
            ),
            const SizedBox(height: 30),
            
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
                   onChange: _onActionParamChange,
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
                   onChange: _onReactionParamChange,
                   formContext: {'service': selectedReactionService!, 'type': 'reactions', 'name': selectedReaction!['name']},
                 )
            ],

            const SizedBox(height: 40),
            
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: _submit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo, 
                  foregroundColor: Colors.white,
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: const Text("CREATE AREA", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}