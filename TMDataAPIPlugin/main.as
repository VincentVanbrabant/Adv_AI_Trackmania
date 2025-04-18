bool Send(Net::Socket@ socket, uint CP, uint time, float speed, int gear, float rpm, float distanceTravelled, vec3 cpPosDelta, vec3 direction) {
	auto buffer = MemoryBuffer(0);

    buffer.Write(CP);
    buffer.Write(time);
    buffer.Write(speed);
    buffer.Write(gear);
    buffer.Write(rpm);
    buffer.Write(distanceTravelled);
    buffer.Write(cpPosDelta.x);
    buffer.Write(cpPosDelta.y);
    buffer.Write(cpPosDelta.z);
    buffer.Write(direction.x);
    buffer.Write(direction.y);
    buffer.Write(direction.z);
    buffer.Write(cpPosDelta.Length());
    buffer.Seek(0, 0);

    return socket.Write(buffer);
}

uint NextLandMark(uint current, uint length) {
    if (current + 1 == length) {
        return 0;
    }
    return current + 1;
}

void Main() {
    uint currentCP = 0;

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
                } else if (playerInfo.EndTime != 0) {
                    currentCP = 4294967295;
                } else {
                    driving = false;
                }
                if (driving) {
                    connected = Send(socket,
                        currentCP,
                        playerInfo.CurrentRaceTime,
                        playerInfo.Speed,
                        playerInfo.EngineCurGear,
                        playerInfo.EngineRpm,
                        playerInfo.Distance,
                        raceData.dMapInfo.MapLandmarks[NextLandMark(playerInfo.LatestCheckpointLandmarkIndex, raceData.dMapInfo.MapLandmarks.Length)].Position - playerInfo.Position,
                        playerInfo.AimDirection
                    );
                }
                yield();
            }
            socket.Close();
			print("Disconnected");
        }
    }
    server_socket.Close();
}
