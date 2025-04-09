void Main()
{
    int8 prevCP = 0;
    int8 currentCP = 0;
    float CPTime = 0.0;

	auto sock_serv = Net::Socket();

	if (!sock_serv.Listen("127.0.0.1", 9000)) {
		print(Time::Now + "Failed to initiate socket");
		return;
	}

	while (!sock_serv.IsReady()) {
		yield();
	}
	print("Socket is ready");

	while (true) {
		auto sock = sock_serv.Accept();
		if (sock is null) yield();
		else {
			print("Connected");
			
			bool cc = true;
			while (cc)
			{
				auto buf = MemoryBuffer(0);
				auto raceData = PlayerState::GetRaceData();
				auto info = raceData.dPlayerInfo;
				if (raceData.PlayerState == PlayerState::EPlayerState::EPlayerState_Driving) {
					currentCP = info.NumberOfCheckpointsPassed;
					if (info.LatestCPTime > 0) {
						CPTime = info.LatestCPTime;
					}
					if (currentCP != 0 && prevCP != currentCP) {
						buf.Write(currentCP);
						buf.Write(info.CurrentRaceTime);
						buf.Seek(0, 0);
				
						cc = sock.Write(buf);
					}

					prevCP = currentCP;
				} else if (info.EndTime != 0) {
					currentCP = 0;

					buf.Write(currentCP);
					buf.Write(info.EndTime);
					buf.Seek(0, 0);
			
					cc = sock.Write(buf);
				}

				yield();
			}
			print("Disconnected");
			sock.Close();
		}
	}
	sock_serv.Close();
}
