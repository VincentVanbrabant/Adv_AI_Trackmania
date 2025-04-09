void Main()
{
    uint8 prevCP = 0;
    uint8 currentCP = 0;
    uint CPTime = 0;

	auto server_socket = Net::Socket();

	if (!server_socket.Listen("127.0.0.1", 9000)) {
		print("Failed to initiate socket");
		return;
	}

	while (!server_socket.IsReady()) yield();

	print("Socket is ready");

	while (true) {
		auto socket = server_socket.Accept();
		if (socket is null) yield();
		else {
			print("Connected");
			
			bool connected = true;
			while (connected) {
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
						buf.Write(CPTime);
						buf.Seek(0, 0);
				
						connected = socket.Write(buf);
					}

					prevCP = currentCP;
				} else if (info.EndTime != 0) {
					currentCP = 0;

					buf.Write(currentCP);
					buf.Write(info.EndTime);
					buf.Seek(0, 0);
			
					connected = socket.Write(buf);
				}

				yield();
			}
			print("Disconnected");
			socket.Close();
		}
	}
	server_socket.Close();
}
