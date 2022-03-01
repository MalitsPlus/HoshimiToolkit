import imp
import caches.master.proto.Skill_pb2 as Skill
from pathlib import Path

skill = Skill.Skill()
pb = Path("caches/master/pb/sk-rio-03-schl-00-1").read_bytes()
skill.ParseFromString(pb)
Path("caches/tmp.json").write_bytes(skill.SerializeToString())
a = 1
