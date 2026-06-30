import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../models/api_models.dart';
import '../providers/lang_provider.dart';
import '../providers/session_provider.dart';

class NodeCFQuestion extends StatelessWidget {
  final ScreenState screen;
  const NodeCFQuestion({super.key, required this.screen});

  static Color _cfColor(double v) {
    if (v >= 0.5) return AppTheme.success;
    if (v > 0) return AppTheme.warning;
    return AppTheme.primary;
  }

  @override
  Widget build(BuildContext context) {
    final lang = context.watch<LangProvider>();
    final session = context.watch<SessionProvider>();
    final isAr = lang.isAr;
    final cf = screen.cf!;

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment:
            isAr ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Text('p.${screen.page}',
              style: const TextStyle(fontSize: 12, color: Color(0xFF4A4A4A))),
          const SizedBox(height: 8),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment:
                    isAr ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                children: [
                  Text(
                    lang.t(screen.text),
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.w600, height: 1.5),
                    textAlign: isAr ? TextAlign.right : TextAlign.left,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    lang.t(cf.prompt),
                    style: const TextStyle(fontSize: 14, height: 1.5, color: Color(0xFF4A4A4A)),
                    textAlign: isAr ? TextAlign.right : TextAlign.left,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          ...cf.choices.map((c) => Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: OutlinedButton(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: _cfColor(c.cfValue),
                    side: BorderSide(color: _cfColor(c.cfValue), width: 1.5),
                  ),
                  onPressed: session.loading
                      ? null
                      : () => session.step(c.id.toString()),
                  child: Row(
                    mainAxisAlignment: isAr
                        ? MainAxisAlignment.end
                        : MainAxisAlignment.spaceBetween,
                    children: isAr
                        ? [
                            Text('CF ${c.cfValue >= 0 ? '+' : ''}${c.cfValue.toStringAsFixed(2)}',
                                style: TextStyle(
                                    fontSize: 11, color: _cfColor(c.cfValue))),
                            const SizedBox(width: 8),
                            Text(lang.t(c.label)),
                          ]
                        : [
                            Text(lang.t(c.label)),
                            Text('CF ${c.cfValue >= 0 ? '+' : ''}${c.cfValue.toStringAsFixed(2)}',
                                style: TextStyle(
                                    fontSize: 11, color: _cfColor(c.cfValue))),
                          ],
                  ),
                ),
              )),
        ],
      ),
    );
  }
}
