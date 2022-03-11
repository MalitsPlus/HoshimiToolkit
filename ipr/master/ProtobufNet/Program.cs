// See https://aka.ms/new-console-template for more information

var stream = File.OpenRead("dec.bin");
QuestStartResponse r = Serializer.Deserialize<QuestStartResponse>(stream);

foreach (var chart in r.result.charts) {
    if (chart.chartType == MusicChartType.Beat) {

    } else if (chart.chartType == MusicChartType.ActiveSkill) {

    } else if (chart.chartType == MusicChartType.SpecialSkill) {

    } else {

    }
    foreach (var status in chart.cardStatuses) {
        status
    }
}
int a = 1;
