import traci
import csv

sumoBinary = r"C:\Users\ABINASH BISWAL\Downloads\sumo-win64-1.27.0\sumo-1.27.0\bin\sumo-gui.exe"

sumoCmd = [
    sumoBinary,
    "-c",
    "simulation/simulation.sumocfg"
]

traci.start(sumoCmd)

with open("data/traffic_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["step", "vehicle_count"])
    file.flush()

    step=0
    while True:
        traci.simulationStep()

        vehicle_count = traci.vehicle.getIDCount()

        writer.writerow([step, vehicle_count])
        file.flush()

        print(f"Step {step}: {vehicle_count}")

        step += 1

traci.close()

print("Dataset created successfully!")