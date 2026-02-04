# GPX Route Generator

This project generates GPX files for GPS location simulation using Google Maps APIs  
It supports realistic movement, instant jumping, and looped routes

---

## Requirements

- Python 3.9 or newer
- Google Maps API key with Geocoding API and Directions API enabled

Install required Python packages 
```
pip install requests gpxpy polyline python-dotenv
```

**Important**: Do not use Python virtual environment (venv) for this project. Xcode may have issues accessing the interpreter. (Currently debugging this issue)
---

## Setup

Create a .env file in project root and add your API key  
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```
---

## Usage

Run script from terminal
python gps_simulator.py [options]

---

## Command Line Arguments
All arguments are optional and default values are provided.

| Argument | Type | Default | Description |
|--------|------|---------|-------------|
| --mode | string | fly | Movement mode: plant, fly, plant_loop (plant_loop uses predefined addresses, not support src & dst arguments) |
| --src | string | 2410 Shakespeare St, Houston, TX 77030 | Starting location. Ignored in fly mode |
| --dst | string | 3915 Kirby Dr, Houston, TX 77098 | Destination location |
| --speed | int | 30 | Recommended default. Change only if needed |
| --interval | float | 0.5 | Recommended default. Change only if needed |
---

## Modes

### plant — Fixed-speed route simulation

Simulates realistic movement along a Google Maps route at constant speed  
GPX points are generated at uniform time intervals

Example usage  
python gps_simulator.py --mode plant --src "2410 Shakespeare St, Houston, TX 77030" --dst "3915 Kirby Dr, Houston, TX 77098"

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

### Using the Generated GPX File

After running gps_simulator.py, you can use the generated route.gpx file for location simulation:

**Xcode (iOS Simulator)**

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
2. In Xcode, go to **Debug** → **Simulate Location** → select **route**
3. The simulator will follow the GPX route automatically
- **Health Data**: The app currently writes 20 steps to HealthKit every 10 seconds when running. To disable this feature, open [ContentView.swift](GPS_Demo/ContentView.swift) and comment out the two HealthManager function calls in the `onAppear` block

**Android Studio (Android Emulator)**
**Note**: This feature has not been tested yet. Welcome feedback and bug reports!
1. Open the emulator's Extended Controls (⋮ button)
2. Go to Location section
3. Click "Load GPX" and select route.gpx
4. Click "Play Route" to start the simulation

---

## Notes

- Locations may be plain text addresses or latitude,longitude pairs
- Google Maps API usage counts toward your quota
- Short routes automatically fall back to simple start and end points

---

## Typical Use Cases

- iOS or Android GPS simulation
- Navigation and tracking app testing
- Replaying realistic or fake GPS movement
