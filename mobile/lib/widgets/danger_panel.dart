import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../models/api_models.dart';
import '../providers/lang_provider.dart';
import '../providers/session_provider.dart';

class DangerPanel extends StatelessWidget {
  const DangerPanel({super.key});

  static const _icons = {
    'b': Icons.water_drop,
    'n': Icons.air,
    'p': Icons.favorite_border,
    'u': Icons.person_off,
  };

  @override
  Widget build(BuildContext context) {
    final lang = context.watch<LangProvider>();
    final session = context.watch<SessionProvider>();
    final panel = session.dangerPanel;

    return Container(
      height: 64,
      decoration: const BoxDecoration(
        color: AppTheme.primary,
        boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 8, offset: Offset(0, -2))],
      ),
      child: Row(
        children: panel.map((item) => _DangerButton(item: item, lang: lang)).toList(),
      ),
    );
  }
}

class _DangerButton extends StatelessWidget {
  final DangerPanelItem item;
  final LangProvider lang;
  const _DangerButton({required this.item, required this.lang});

  @override
  Widget build(BuildContext context) {
    final session = context.read<SessionProvider>();
    return Expanded(
      child: InkWell(
        onTap: session.isAlive && !session.loading
            ? () => session.step(item.key)
            : null,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              DangerPanel._icons[item.key] ?? Icons.warning,
              color: Colors.white,
              size: 20,
            ),
            const SizedBox(height: 2),
            Text(
              lang.t(item.label),
              style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w600),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }
}
