import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/api_models.dart';
import '../providers/lang_provider.dart';
import '../providers/session_provider.dart';

class NodeInstruction extends StatelessWidget {
  final ScreenState screen;
  const NodeInstruction({super.key, required this.screen});

  @override
  Widget build(BuildContext context) {
    final lang = context.watch<LangProvider>();
    final session = context.watch<SessionProvider>();
    final isAr = lang.isAr;

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment:
            isAr ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          _pageTag(screen.page),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Text(
                lang.t(screen.text),
                style: const TextStyle(fontSize: 16, height: 1.6),
                textAlign: isAr ? TextAlign.right : TextAlign.left,
              ),
            ),
          ),
          const Spacer(),
          ElevatedButton(
            onPressed: session.loading ? null : () => session.step('1'),
            child: Text(isAr ? 'متابعة' : 'Continue'),
          ),
        ],
      ),
    );
  }
}

Widget _pageTag(int page) => Text(
      'p.$page',
      style: const TextStyle(fontSize: 12, color: Color(0xFF4A4A4A)),
    );
