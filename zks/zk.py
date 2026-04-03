from imports.get_shared_mem import get_shared_mem
from imports.get_extended_shared_mem import read_data_from_shared_memory

import os

info = get_shared_mem()

numVehicles, focusVehicle, serverName, pluginVersion, isInternalMemoryModuleLoaded, acInstallPath, drivers_inf = read_data_from_shared_memory()


while True:
    print(info.physics.brake)