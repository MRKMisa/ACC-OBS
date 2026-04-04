"""
SimHub SharedMemory
Based on CrewChief work (Sparten)
No licence apply.
"""
import mmap
import os
import struct
import functools
import ctypes
from ctypes import c_float, c_char, c_int32

class vec3(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ]

class acsVehicleInfo(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('carId', c_int32),
        ('driverName', c_char * 64),
        ('carModel', c_char * 64),
        ('speedMS', c_float),
        ('bestLapMS', c_int32),
        ('lapCount', c_int32),
        ('currentLapInvalid', c_int32),
        ('currentLapTimeMS', c_int32),
        ('lastLapTimeMS', c_int32),
        ('worldPosition', vec3),
        ('isCarInPitline', c_int32),
        ('isCarInPit', c_int32  ),
        ('carLeaderboardPosition', c_int32),
        ('carRealTimeLeaderboardPosition', c_int32),
        ('spLineLength', c_float),
        ('isConnected', c_int32),
        ('suspensionDamage', c_float * 4),
        ('engineLifeLeft', c_float),
        ('tyreInflation', c_float * 4),
    ]
      
class SPageFileSimHub(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('numVehicles', c_int32),
        ('focusVehicle', c_int32),
        ('serverName', c_char * 512),
        ('vehicleInfo', acsVehicleInfo * 64),
        ('acInstallPath', c_char * 512),
        ('isInternalMemoryModuleLoaded', c_int32),
        ('pluginVersion', c_char * 32)		
    ]

class SimHubShared:
    def __init__(self):
        self._acpmf_simhub = mmap.mmap(0, ctypes.sizeof(SPageFileSimHub),"acpmf_simhub")
        self.simhub = SPageFileSimHub.from_buffer(self._acpmf_simhub)
              
    def close(self):
        #self._acpmf_simhub.close()
        pass

    def __del__(self):
        #self.close()
        pass
            
    def getsharedmem(self):
        return self.simhub

import os

global drivers_inf


def read_data_from_shared_memory():
    shared_memory = SimHubShared()
    drivers_inf = []

    try:
        # Získání aktuálních dat ze sdílené paměti
        shared_data = shared_memory.getsharedmem()

        numVehicles = shared_data.numVehicles
        focusVehicle = shared_data.focusVehicle
        vehicleInfoArray = shared_data.vehicleInfo
        serverName = shared_data.serverName.decode('utf-8')
        pluginVersion = shared_data.pluginVersion.decode('utf-8')
        isInternalMemoryModuleLoaded = bool(shared_data.isInternalMemoryModuleLoaded)
        acInstallPath = shared_data.acInstallPath.decode('utf-8')

        # Výpis informací o každém vozidle
        for i in range(shared_data.numVehicles):
            vehicle = shared_data.vehicleInfo[i]

            drivers_inf.append({"Index":i + 1, "ID":vehicle.carId, "DriverName":vehicle.driverName.decode('utf-8'), "CarModel":vehicle.carModel.decode('utf-8'), "SpeedMS":vehicle.speedMS, "SpeedKMH":int(vehicle.speedMS)*3.6, "BestLapMS":vehicle.bestLapMS, "LapCount":vehicle.lapCount, "IsCurrentLapInvalid":bool(vehicle.currentLapInvalid), "CurrentlapTimeMS":vehicle.currentLapTimeMS, "LastLapTimeMS":vehicle.lastLapTimeMS, "WorldPosX": vehicle.worldPosition.x ,"WorldPosY": vehicle.worldPosition.y, "WorldPosZ": vehicle.worldPosition.z, "IsCarInPitLine":bool(vehicle.isCarInPitline), "IsCarInPit":bool(vehicle.isCarInPit), "LeaderBoardPos":vehicle.carLeaderboardPosition, "RealLeaderBoardPos":vehicle.carRealTimeLeaderboardPosition, "SPLineLenght":vehicle.spLineLength, "IsConnected":bool(vehicle.isConnected), "SuspensionDamage":list(vehicle.suspensionDamage), "EngineLifeLeft":vehicle.engineLifeLeft, "TyrePSI":list(vehicle.tyreInflation)})
            
        return numVehicles, focusVehicle, serverName, pluginVersion, isInternalMemoryModuleLoaded, acInstallPath, drivers_inf

    except KeyboardInterrupt:
        print("Čtení bylo přerušeno uživatelem.")

        
