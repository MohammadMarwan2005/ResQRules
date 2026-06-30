class BilingualText {
  final String en;
  final String ar;
  const BilingualText({required this.en, required this.ar});

  factory BilingualText.fromJson(Map<String, dynamic> j) =>
      BilingualText(en: j['en'] ?? '', ar: j['ar'] ?? '');

  String t(String lang) => lang == 'ar' ? ar : en;
}

class OptionItem {
  final int id;
  final BilingualText label;
  const OptionItem({required this.id, required this.label});

  factory OptionItem.fromJson(Map<String, dynamic> j) =>
      OptionItem(id: j['id'], label: BilingualText.fromJson(j['label']));
}

class CFChoice {
  final int id;
  final String key;
  final BilingualText label;
  final double cfValue;
  const CFChoice(
      {required this.id,
      required this.key,
      required this.label,
      required this.cfValue});

  factory CFChoice.fromJson(Map<String, dynamic> j) => CFChoice(
      id: j['id'],
      key: j['key'],
      label: BilingualText.fromJson(j['label']),
      cfValue: (j['cf_value'] as num).toDouble());
}

class CFConfig {
  final BilingualText prompt;
  final List<CFChoice> choices;
  final double threshold;
  const CFConfig(
      {required this.prompt, required this.choices, required this.threshold});

  factory CFConfig.fromJson(Map<String, dynamic> j) => CFConfig(
      prompt: BilingualText.fromJson(j['prompt']),
      choices:
          (j['choices'] as List).map((c) => CFChoice.fromJson(c)).toList(),
      threshold: (j['threshold'] as num).toDouble());
}

class HemTierInfo {
  final int current;
  final int maxTier;
  final bool terminal;
  final BilingualText intervention;
  const HemTierInfo(
      {required this.current,
      required this.maxTier,
      required this.terminal,
      required this.intervention});

  factory HemTierInfo.fromJson(Map<String, dynamic> j) => HemTierInfo(
      current: j['current'],
      maxTier: j['max_tier'],
      terminal: j['terminal'],
      intervention: BilingualText.fromJson(j['intervention']));
}

class DangerPanelItem {
  final String key;
  final BilingualText label;
  final String severity;
  const DangerPanelItem(
      {required this.key, required this.label, required this.severity});

  factory DangerPanelItem.fromJson(Map<String, dynamic> j) => DangerPanelItem(
      key: j['key'],
      label: BilingualText.fromJson(j['label']),
      severity: j['severity']);
}

class OverrideEvent {
  final String kind;
  final int salience;
  final String? jumpedToChart;
  final bool guardFired;
  const OverrideEvent(
      {required this.kind,
      required this.salience,
      this.jumpedToChart,
      required this.guardFired});

  factory OverrideEvent.fromJson(Map<String, dynamic> j) => OverrideEvent(
      kind: j['kind'],
      salience: j['salience'],
      jumpedToChart: j['jumped_to_chart'],
      guardFired: j['guard_fired']);
}

class ScreenState {
  final String type;
  final String nodeId;
  final String chartId;
  final BilingualText chartTitle;
  final int page;
  final BilingualText text;
  final List<OptionItem>? options;
  final CFConfig? cf;
  final HemTierInfo? hemTier;
  final bool isTerminal;
  final String? stubTarget;

  const ScreenState({
    required this.type,
    required this.nodeId,
    required this.chartId,
    required this.chartTitle,
    required this.page,
    required this.text,
    this.options,
    this.cf,
    this.hemTier,
    this.isTerminal = false,
    this.stubTarget,
  });

  factory ScreenState.fromJson(Map<String, dynamic> j) => ScreenState(
      type: j['type'],
      nodeId: j['node_id'],
      chartId: j['chart_id'],
      chartTitle: BilingualText.fromJson(j['chart_title']),
      page: j['page'],
      text: BilingualText.fromJson(j['text']),
      options: j['options'] != null
          ? (j['options'] as List).map((o) => OptionItem.fromJson(o)).toList()
          : null,
      cf: j['cf'] != null ? CFConfig.fromJson(j['cf']) : null,
      hemTier:
          j['hem_tier'] != null ? HemTierInfo.fromJson(j['hem_tier']) : null,
      isTerminal: j['is_terminal'] ?? false,
      stubTarget: j['stub_target']);
}

class SessionResponse {
  final String sessionId;
  final bool alive;
  final ScreenState screen;
  final OverrideEvent? overrideEvent;
  final List<DangerPanelItem> dangerPanel;

  const SessionResponse({
    required this.sessionId,
    required this.alive,
    required this.screen,
    this.overrideEvent,
    required this.dangerPanel,
  });

  factory SessionResponse.fromJson(Map<String, dynamic> j) => SessionResponse(
      sessionId: j['session_id'],
      alive: j['alive'],
      screen: ScreenState.fromJson(j['screen']),
      overrideEvent: j['override_event'] != null
          ? OverrideEvent.fromJson(j['override_event'])
          : null,
      dangerPanel: (j['danger_panel'] as List)
          .map((d) => DangerPanelItem.fromJson(d))
          .toList());
}

class ChartInfo {
  final String chartId;
  final BilingualText title;
  final String urgency;
  const ChartInfo(
      {required this.chartId, required this.title, required this.urgency});

  factory ChartInfo.fromJson(Map<String, dynamic> j) => ChartInfo(
      chartId: j['chart_id'],
      title: BilingualText.fromJson(j['title']),
      urgency: j['urgency']);
}
