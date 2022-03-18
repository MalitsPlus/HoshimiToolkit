
void decryptTraffic() {
    byte[] data = CryptoHelper.get().doDecrypt("QuestStartResponse/queststart220318164520987.bin");
    //File.WriteAllBytes("userdata.bin", data);
    JsonHelper.generateJson<QuestStartResponse>(data, "queststart220318164520987");
}

void deserializeProto() {
    string pathStr = "StaffLevel";
    JsonHelper.generateJsonDir<StaffLevel>(pathStr);
}

decryptTraffic();
//deserializeProto();
int a = 0;