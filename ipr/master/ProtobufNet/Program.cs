void generateJson<T>(string pathStr) {
    List<T> list = new List<T>();
    DirectoryInfo directoryInfo = new DirectoryInfo(pathStr);
    foreach (var file in directoryInfo.EnumerateFiles()) {
        using (var stream = file.OpenRead()) {
            var obj = Serializer.Deserialize<T>(stream);
            list.Add(obj);
        }
    }
    var options = new JsonSerializerOptions { WriteIndented = true };
    string s = JsonSerializer.Serialize(list, options);

    string output = $"json/{pathStr}.json";
    File.WriteAllText(output, s);
}

string pathStr = "Setting";
generateJson<Setting>(pathStr);
int a = 0;