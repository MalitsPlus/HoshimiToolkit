import imp
import live_tip_pb2
from pathlib import Path

live_tip = live_tip_pb2.LiveTip()
pb = Path("caches/master/pb/live_tip-low_activating_rate-01").read_bytes()
live_tip.ParseFromString(pb)
a = 1
