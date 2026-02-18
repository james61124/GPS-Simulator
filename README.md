# GPX Route Generator

This project generates GPX files for GPS location simulation using Google Maps APIs  
It supports realistic movement, instant jumping, and looped routes

---

## Requirements

- Python 3.9 or newer
- Google Maps API key. There is a free quota. Register at [Google Cloud](https://console.cloud.google.com/welcome?project=gps-demo-486121) and enable the **Geocoding API** and **Directions API**.
---

## Setup
1. Install required Python packages

	**Important:** Do not use Python virtual environment (venv) for this project. Xcode may have issues accessing the interpreter. (Currently debugging this issue)

	```
	pip install requests gpxpy polyline python-dotenv
	```

2. Create a .env file in project root and add your API key

	```
	GOOGLE_MAPS_API_KEY=your_api_key_here
	```
---

## Usage

1. Run script from terminal: 
```python gps_simulator.py [options]```
2. Use the generated GPX file for simulation (details below).
3. Run the app on your device, enter the desired steps, and click **Add Steps Now**.

---

## Command Line Arguments
All arguments are optional and default values are provided.

You can use plain text addresses or latitude/longitude for `--src` and `--dst`, e.g. "29.7341222, -95.4223470". For addresses, remove special symbols.

| Argument | Type | Default | Description |
|--------|------|---------|-------------|
| --mode | string | fly | Movement mode: plant, fly, plant_loop (plant_loop uses predefined addresses, not support src & dst arguments) |
| --src | string | 2410 Shakespeare St, Houston, TX 77030 | Starting location. Ignored in fly & plant_loop mode |
| --dst | string | 3915 Kirby Dr, Houston, TX 77098 | Destination location. Ignored in plant_loop mode |
| --speed | int | 30 | Recommended default. Change only if needed |
| --interval | float | 0.5 | Recommended default. Change only if needed |


---

## Modes

### plant — Fixed-speed route simulation

Simulates realistic movement along a Google Maps route at constant speed  
GPX points are generated at uniform time intervals

Example usage  
python gps_simulator.py --mode plant --src "2410 Shakespeare St, Houston, TX 77030" --dst "29.7341222, -95.4223470"

---

### fly — Jump mode

Instantly moves from source to destination with minimal time difference  
Useful when only final location matters

Example usage  
python gps_simulator.py --mode fly --dst "Kirby Dr, Houston, TX 77098"

---

### plant_loop — Looping route simulation

Moves through multiple predefined addresses in a loop  
Speed and interval behave the same as plant mode  
Addresses are currently defined in main()

Example usage  
python gps_simulator.py --mode plant_loop

---

## Output

- Generated file name: route.gpx
- GPX contains waypoints with timestamps
- Compatible with Xcode, Android Studio, and most GPS simulators

## Using the Generated GPX File

After running gps_simulator.py, you can use the generated route.gpx file for location simulation:

### Xcode (iOS Simulator)

**First-time setup:**
1. On your iPhone, go to Settings → Privacy & Security and enable **Developer Mode**
2. Open this repository in Xcode
3. In Xcode, select the project in the navigator, go to **Signing & Capabilities** tab
   - Select your Apple ID as the Team
   - Change the Bundle Identifier to something unique (e.g., `com.yourname.gps-demo`)
4. Connect your iPhone to your Mac via USB cable
5. At the top of Xcode, click the device selector (shows current target) and select your iPhone
6. Click the **Build and Run** button (the ▶ play icon in the top toolbar)
7. On your iPhone, go to Settings → General → **VPN & Device Management** and tap **Trust** to verify the app

**Running the GPS simulation:**
1. Generate a GPX file using the gps_simulator.py script
2. Import to Xcode and wait for launch (until your iPhone opens the app) 
3. Configure Auto-Start in Xcode (Optional):
	- Go to Product → Scheme → Edit Scheme
	- Select Run > Options and check Allow Location Simulation.
	- Set Default Location to your route file.
4. Manual Start in Xcode:
	- go to **Debug** → **Simulate Location** → select **route**
5. Success: The simulator will follow the GPX route automatically

### Android Studio (Android Emulator)

**Note**: This feature has not been tested yet. Welcome feedback and bug reports!
1. Open the emulator's Extended Controls (⋮ button)
2. Go to Location section
3. Click "Load GPX" and select route.gpx
4. Click "Play Route" to start the simulation

---

## Notes

- Google Maps API usage counts toward your quota
- Short routes automatically fall back to simple start and end points

---

## Typical Use Cases

- iOS or Android GPS simulation
- Navigation and tracking app testing
- Replaying realistic or fake GPS movement
