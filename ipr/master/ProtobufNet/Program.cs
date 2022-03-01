// See https://aka.ms/new-console-template for more information


var stream = File.OpenRead("sk-ngs-05-idol-00-3");
Skill skill = Serializer.Deserialize<Skill>(stream);
int a = 1;