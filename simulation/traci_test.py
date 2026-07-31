import traci

sumoBinary = r"C:\Users\ABINASH BISWAL\Downloads\sumo-win64-1.27.0\sumo-1.27.0\bin\sumo-gui.exe"

sumoCmd = [
    sumoBinary,
    "-c",
    "simulation/simulation.sumocfg"
]

traci.start(sumoCmd)

for step in range(100):
    traci.simulationStep()

    vehicle_count = traci.vehicle.getIDCount()

    print(f"Step {step}: Vehicles = {vehicle_count}")

traci.close()