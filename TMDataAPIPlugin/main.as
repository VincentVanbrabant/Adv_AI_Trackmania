bool Send(Net::Socket@ socket, uint CP, uint time) {
	auto buffer = MemoryBuffer(0);

    buffer.Write(CP);
    buffer.Write(time);
    buffer.Seek(0, 0);

    return socket.Write(buffer);
}

void Main() {
    uint previousCP = 0;
    uint currentCP = 0;
    uint CPTime = 0;

    auto server_socket = Net::Socket();

    if (!server_socket.Listen("127.0.0.1", 9000)) {
        print("Failed to initiate server");
        return;
    }

    while (!server_socket.IsReady()) yield();
    print("Server is ready");

    while (true) {
        auto socket = server_socket.Accept();
        if (socket is null) yield();
        else {
            print("Connected");

            bool connected = true;
            while (connected && !socket.IsHungUp()) {
                auto raceData = PlayerState::GetRaceData();
                auto playerInfo = raceData.dPlayerInfo;
                bool driving = true;
                if (raceData.PlayerState == PlayerState::EPlayerState::EPlayerState_Driving) {
                    currentCP = playerInfo.NumberOfCheckpointsPassed;

                    if (playerInfo.LatestCPTime > 0) {
                        CPTime = playerInfo.LatestCPTime;
                    }
                    if (currentCP != 0 && previousCP != currentCP) {
						previousCP = currentCP;

                        // connected = Send(socket, currentCP, CPTime);
                    }
                } else if (playerInfo.EndTime != 0) {
                    currentCP = 4294967295;

                    // connected = Send(socket, currentCP, playerInfo.EndTime);
                } else {
                    driving = false;
                }
                if (driving) {
                    connected = Send(socket, currentCP, playerInfo.CurrentRaceTime);
                }
                yield();
            }
            socket.Close();
			print("Disconnected");
        }
    }
    server_socket.Close();
}
