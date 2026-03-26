import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DynamicForm extends StatelessWidget {
  final Map<String, dynamic> schema;
  final Map<String, dynamic> values;
  final Function(String key, dynamic value) onChange;
  final Map<String, String> formContext;

  const DynamicForm({
    super.key,
    required this.schema,
    required this.values,
    required this.onChange,
    required this.formContext,
  });

  @override
  Widget build(BuildContext context) {
    if (schema.isEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(top: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey.shade300),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "⚙️ Configure ${formContext['type'] == 'actions' ? 'Trigger' : 'Action'}", 
            style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.indigo, fontSize: 13)
          ),
          const SizedBox(height: 10),
          ...schema.entries.map((entry) {
            return DynamicField(
              fieldKey: entry.key,
              fieldDef: entry.value,
              value: values[entry.key],
              onChange: onChange,
              formContext: formContext,
            );
          }),
        ],
      ),
    );
  }
}

class DynamicField extends StatefulWidget {
  final String fieldKey;
  final Map<String, dynamic> fieldDef;
  final dynamic value;
  final Function(String key, dynamic value) onChange;
  final Map<String, String> formContext;

  const DynamicField({
    super.key,
    required this.fieldKey,
    required this.fieldDef,
    required this.value,
    required this.onChange,
    required this.formContext,
  });

  @override
  State<DynamicField> createState() => _DynamicFieldState();
}

class _DynamicFieldState extends State<DynamicField> {
  List<dynamic> options = [];
  bool loading = false;

  @override
  void initState() {
    super.initState();
    if (widget.fieldDef['type'] == 'select' && widget.fieldDef.containsKey('dynamic_source')) {
      _fetchOptions();
    }
  }

  void _fetchOptions() async {
    setState(() => loading = true);
    try {
      final endpoint = "/services/${widget.formContext['service']}/${widget.formContext['type']}/${widget.formContext['name']}/options/${widget.fieldKey}";
      final data = await ApiService.get(endpoint);
      if (mounted) {
        setState(() {
          options = data;
          loading = false;
        });
      }
    } catch (e) {
      debugPrint("Error loading options: $e");
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final label = widget.fieldDef['title'] ?? widget.fieldKey.replaceAll('_', ' ').toUpperCase();
    final type = widget.fieldDef['type'] ?? 'string';

    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 12, color: Colors.grey)),
          const SizedBox(height: 4),
          _buildInput(type),
        ],
      ),
    );
  }

  Widget _buildInput(String type) {
    if (type == 'select') {
      return InputDecorator(
        decoration: InputDecoration(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 0),
        ),
        child: DropdownButtonHideUnderline(
          child: DropdownButton<String>(
            value: widget.value != null && widget.value.toString().isNotEmpty ? widget.value.toString() : null,
            isExpanded: true,
            hint: Text(loading ? "Loading..." : "Select option"),
            items: options.map<DropdownMenuItem<String>>((opt) {
              return DropdownMenuItem(
                value: opt['value'].toString(),
                child: Text(opt['label'].toString()),
              );
            }).toList(),
            onChanged: (val) => widget.onChange(widget.fieldKey, val),
          ),
        ),
      );
    }

    return TextFormField(
      initialValue: widget.value?.toString() ?? widget.fieldDef['default']?.toString() ?? '',
      keyboardType: type == 'number' ? TextInputType.number : TextInputType.text,
      decoration: InputDecoration(
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
      ),
      onChanged: (val) => widget.onChange(widget.fieldKey, val),
    );
  }
}