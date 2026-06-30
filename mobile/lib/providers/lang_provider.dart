import 'package:flutter/foundation.dart';
import '../models/api_models.dart';

class LangProvider extends ChangeNotifier {
  String _lang = 'en';

  String get lang => _lang;
  bool get isAr => _lang == 'ar';

  String t(BilingualText text) => isAr ? text.ar : text.en;

  void toggle() {
    _lang = isAr ? 'en' : 'ar';
    notifyListeners();
  }
}
