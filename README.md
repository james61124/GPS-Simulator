# GPX Route Generator

This project generates GPX files for GPS location simulation using Google Maps APIs  
It supports realistic movement, instant teleporting, and looped routes

---

## Requirements

- Python 3.9 or newer
- Google Maps API key with Geocoding API and Directions API enabled

Install required Python packages 
```
pip install requests gpxpy polyline python-dotenv
```
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
| --mode | string | fly | Movement mode: plant, fly, plant_loop |
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

### fly — Teleport mode

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
1. Build and run your iOS app in Xcode
2. Go to Debug → Simulate Location → select route
3. The simulator will follow the GPX route automatically

**Android Studio (Android Emulator)**
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
