import struct

class TrackmaniaAPIData:
    def __init__(self, response: bytes):
        self.cp   = struct.unpack('I', response[-52:-48])[0]
        self.time = struct.unpack('I', response[-48:-44])[0]

        self.speed = struct.unpack('f', response[-44:-40])[0]
        self.gear  = struct.unpack('i', response[-40:-36])[0]
        self.rpm   = struct.unpack('f', response[-36:-32])[0]

        self.distanceTravelled = struct.unpack('f', response[-32:-28])[0]

        self.cp_pos_delta = (
            struct.unpack('f', response[-28:-24])[0],
            struct.unpack('f', response[-24:-20])[0],
            struct.unpack('f', response[-20:-16])[0],
        )

        self.direction = (
            struct.unpack('f', response[-16:-12])[0],
            struct.unpack('f', response[-12:-8])[0],
            struct.unpack('f', response[-8:-4])[0],
        )

        self.distance_to_cp = struct.unpack('f', response[-4:])[0]
