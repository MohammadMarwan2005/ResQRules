import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/api_models.dart';
import '../providers/lang_provider.dart';
import '../providers/session_provider.dart';

class NodeQuestion extends StatelessWidget {
  final ScreenState screen;
  const NodeQuestion({super.key, required this.screen});

  @override
  Widget build(BuildContext context) {
    final lang = context.watch<LangProvider>();
    final session = context.watch<SessionProvider>();
    final isAr = lang.isAr;
    final options = screen.options ?? [];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment:
            isAr ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Text(
            'p.${screen.page}',
            style: const TextStyle(fontSize: 12, color: Color(0xFF4A4A4A)),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Text(
                lang.t(screen.text),
                style: const TextStyle(
                    fontSize: 16, fontWeight: FontWeight.w600, height: 1.5),
                textAlign: isAr ? TextAlign.right : TextAlign.left,
              ),
            ),
          ),
          const SizedBox(height: 16),
          ...options.map((opt) => Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: OutlinedButton(
                  onPressed: session.loading
                      ? null
                      : () => session.step(opt.id.toString()),
                  child: Text(lang.t(opt.label)),
                ),
              )),
        ],
      ),
    );
  }
}
