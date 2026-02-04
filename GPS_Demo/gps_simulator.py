"""
Main script to create GPX file (2 modes)
Mode 1: fixed-speed along route
Mode 2: jump to destination
"""

import os
import requests
import gpxpy
import gpxpy.gpx
import polyline
import datetime
import random
import math
import argparse

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise ImportError(
        "python-dotenv is not installed.\n"
        "Install it with: pip install python-dotenv"
    ) from e

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # environment variable name

if not API_KEY:
    raise RuntimeError(
        "Environment variable GOOGLE_MAPS_API_KEY not found.\n"
        "Please add GOOGLE_MAPS_API_KEY=your_api_key to the .env file"
    )

ARG_SPECS = [
    {
        "flags": ["--mode"],
        "type": str,
        "choices": ["plant", "fly", "plant_loop"],
        "default": "fly",
        "help": "Movement mode: plant, fly, plant_loop (plant_loop uses predefined addresses, not support src & dst arguments)",
    },
    {
        "flags": ["--src"],
        "type": str,
        "default": "2410 Shakespeare St, Houston, TX 77030",
        "help": "Starting location. Ignored in fly mode",
    },
    {
        "flags": ["--dst"],
        "type": str,
        "default": "3915 Kirby Dr, Houston, TX 77098",
        "help": "Destination location",
    },
    {
        "flags": ["--speed"],
        "type": int,
        "default": 30,
        "help": "Recommended default. Change only if needed",
    },
    {
        "flags": ["--interval"],
        "type": float,
        "default": 0.5,
        "help": "Recommended default. Change only if needed",
    },
]

def add_cli_arguments(parser):
    for spec in ARG_SPECS:
        flags = spec["flags"]
        kwargs = {
            "type": spec["type"],
            "default": spec["default"],
            "help": spec["help"],
        }
        if "choices" in spec:
            kwargs["choices"] = spec["choices"]
        parser.add_argument(*flags, **kwargs)
    return parser

def parse_args():
    parser = argparse.ArgumentParser()
    add_cli_arguments(parser)
    return parser.parse_args()

def steps_to_route_points(steps):
    route_points = []
    for step in steps:
        pts = decode_polyline(step["polyline"]["points"])
        if not pts:
            continue
        if route_points:
            pts = pts[1:]  # drop duplicate joint point
        route_points.extend(pts)
    return route_points

def interpolate_point(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def densify_by_time(points, speed_mps, interval_s):
    if not points or len(points) < 2:
        return points or []

    spacing_m = speed_mps * interval_s
    out = [points[0]]

    cur = points[0]
    seg_i = 0

    while seg_i < len(points) - 1:
        nxt = points[seg_i + 1]
        seg_len = haversine_m(cur[0], cur[1], nxt[0], nxt[1])

        if seg_len < 1e-6:
            seg_i += 1
            cur = nxt
            continue

        if seg_len >= spacing_m:
            t = spacing_m / seg_len
            cur = interpolate_point(cur, nxt, t)
            out.append(cur)
        else:
            seg_i += 1
            cur = nxt

    if haversine_m(out[-1][0], out[-1][1], points[-1][0], points[-1][1]) > 0.5:
        out.append(points[-1])

    return out

def get_coordinates(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url, timeout=20)
    data = response.json()
    if data.get("status") == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    raise Exception(f"Error fetching coordinates: {data.get('status')} | {data.get('error_message')}")

def get_route_steps(origin, destination):
    url = (
        "https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&departure_time=now&key={API_KEY}"
    )
    response = requests.get(url, timeout=20)
    data = response.json()
    if data.get("status") == "OK":
        return data["routes"][0]["legs"][0]["steps"]
    raise Exception(f"Error fetching route: {data.get('status')} | {data.get('error_message')}")

def decode_polyline(polyline_str):
    return polyline.decode(polyline_str)

def add_pause_waypoints(gpx, destination_coords, current_time, pause_hours):
    pause_duration = pause_hours * 3600
    num_pause_points = pause_hours * 60  # 1 point per minute
    if num_pause_points <= 0:
        return current_time

    for _ in range(num_pause_points):
        current_time += datetime.timedelta(seconds=pause_duration / num_pause_points)
        altered_coords = (
            destination_coords[0] + 1e-8 * random.random(),
            destination_coords[1] + 1e-8 * random.random(),
        )
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(altered_coords[0], altered_coords[1], time=current_time))

    return current_time

def create_gpx_mode1_fixed_speed(origin_coords, destination_coords, steps, speed_kmh, interval_s, pause_hours):
    gpx = gpxpy.gpx.GPX()
    current_time = datetime.datetime.now()

    # collect all route points across steps into one polyline
    route_points = []
    for step in steps:
        pts = decode_polyline(step["polyline"]["points"])
        if not pts:
            continue
        if route_points:
            pts = pts[1:]  # drop duplicate joint point
        route_points.extend(pts)

    # fallback if route too short
    if len(route_points) < 2:
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(origin_coords[0], origin_coords[1], time=current_time))
        current_time += datetime.timedelta(seconds=1)
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(destination_coords[0], destination_coords[1], time=current_time))
        current_time = add_pause_waypoints(gpx, destination_coords, current_time, pause_hours)
        return gpx

    speed_mps = speed_kmh * 1000 / 3600
    dense_points = densify_by_time(route_points, speed_mps, interval_s)

    # emit waypoints with uniform timestamps
    for p in dense_points:
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(p[0], p[1], time=current_time))
        current_time += datetime.timedelta(seconds=interval_s)

    # ensure destination exists as last point
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(destination_coords[0], destination_coords[1], time=current_time))

    # pause at destination
    current_time = add_pause_waypoints(gpx, destination_coords, current_time, pause_hours)
    return gpx

def create_gpx_mode2_jump(origin_coords, destination_coords, pause_hours, jump_seconds=1):
    gpx = gpxpy.gpx.GPX()
    current_time = datetime.datetime.now()

    # start point
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(origin_coords[0], origin_coords[1], time=current_time))

    # "jump" to destination quickly
    current_time += datetime.timedelta(seconds=jump_seconds)
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(destination_coords[0], destination_coords[1], time=current_time))

    # pause at destination
    current_time = add_pause_waypoints(gpx, destination_coords, current_time, pause_hours)
    return gpx

def create_gpx_mode3_loop(addresses, laps, speed_kmh, interval_s, pause_each_stop_hours=0):
    """
    addresses: list[str]  like [A1, A2, A3, A4]
    laps: int  number of loops
    output path: 1->2->3->4->1  repeat laps times
    """
    if not addresses or len(addresses) < 2:
        raise ValueError("Mode 3 needs at least 2 addresses")

    # geocode once
    coords = [get_coordinates(addr) for addr in addresses]

    gpx = gpxpy.gpx.GPX()
    current_time = datetime.datetime.now()

    speed_mps = speed_kmh * 1000 / 3600

    # start at first address
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(coords[0][0], coords[0][1], time=current_time))

    for lap in range(laps):
        for i in range(len(coords)):
            a = coords[i]
            b = coords[(i + 1) % len(coords)]  # close loop

            steps = get_route_steps(f"{a[0]},{a[1]}", f"{b[0]},{b[1]}")
            route_points = steps_to_route_points(steps)

            # ensure join is smooth with previous point in gpx
            if route_points and len(route_points) >= 2:
                dense = densify_by_time(route_points, speed_mps, interval_s)

                # drop first point to avoid duplicate with last written
                dense = dense[1:] if len(dense) > 1 else dense

                for p in dense:
                    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(p[0], p[1], time=current_time))
                    current_time += datetime.timedelta(seconds=interval_s)

            # optional pause at each stop b
            if pause_each_stop_hours > 0:
                current_time = add_pause_waypoints(gpx, b, current_time, pause_each_stop_hours)

    return gpx

def main():
    pause_hours = 1

    args = parse_args()
    mode = args.mode
    src = args.src
    dst = args.dst
    speed_kmh = args.speed
    interval_s = args.interval

    origin_coords = get_coordinates(src)
    destination_coords = get_coordinates(dst)

    if mode == "plant":
        steps = get_route_steps(f"{origin_coords[0]},{origin_coords[1]}", f"{destination_coords[0]},{destination_coords[1]}")
        gpx = create_gpx_mode1_fixed_speed(
            origin_coords=origin_coords,
            destination_coords=destination_coords,
            steps=steps,
            speed_kmh=speed_kmh,
            interval_s=interval_s,
            pause_hours=pause_hours,
        )
    elif mode == "fly":
        jump_seconds = 1  # change to 0 if target accepts same timestamp
        gpx = create_gpx_mode2_jump(
            origin_coords=origin_coords,
            destination_coords=destination_coords,
            pause_hours=pause_hours,
            jump_seconds=jump_seconds,
        )
    elif mode == "plant_loop":
        addresses = [
            "2410 Shakespeare St, Houston, TX 77030",
            "2301 University Blvd, Houston, TX 77005",
            "6010 Greenbriar Dr, Houston, TX 77030",
            "2729 Pemberton Dr, Houston, TX 77005",
            "2740 University Blvd, Houston, TX 77005",
        ]
        laps = 1
        pause_each_stop_hours = 0  # set to 1 if you want 1 hour stop at every node

        gpx = create_gpx_mode3_loop(
            addresses=addresses,
            laps=laps,
            speed_kmh=speed_kmh,
            interval_s=interval_s,
            pause_each_stop_hours=pause_each_stop_hours,
        )
    else:
        raise ValueError("MODE must be plant, fly, or plant_loop")

    with open("route.gpx", "w") as f:
        f.write(gpx.to_xml())

    print("GPX file created successfully: route.gpx")

if __name__ == "__main__":
    main()

