"""Week 1 Client Project: Average Temperature Data Processing Script."""

from typing import Dict, List, Tuple


def compute_temperature_stats(readings: List[float]) -> Tuple[float, float, float]:
    """Return (min_temp, max_temp, avg_temp) for a non-empty list of readings."""
    if not readings:
        raise ValueError("Temperature readings list cannot be empty.")

    total = 0.0
    min_temp = readings[0]
    max_temp = readings[0]

    for temp in readings:
        total += temp
        if temp < min_temp:
            min_temp = temp
        if temp > max_temp:
            max_temp = temp

    avg_temp = total / len(readings)
    return min_temp, max_temp, avg_temp


def count_above_threshold(readings: List[float], threshold: float) -> int:
    """Count how many readings strictly exceed the given threshold."""
    count = 0
    idx = 0
    while idx < len(readings):
        if readings[idx] > threshold:
            count += 1
        idx += 1
    return count


def main() -> None:
    """Process weekly temperature readings across multiple client weather stations."""
    station_readings: Dict[str, List[float]] = {
        "Station_North": [18.5, 19.2, 21.0, 22.4, 20.8, 19.9, 21.5],
        "Station_Central": [24.1, 25.6, 26.8, 27.3, 25.9, 24.7, 26.2],
        "Station_South": [29.4, 30.1, 31.5, 32.0, 30.8, 29.9, 31.2],
    }
    alert_threshold = 28.0

    print("=== Client Temperature Data Processing Report ===")
    overall_readings: List[float] = []

    for station, temps in station_readings.items():
        min_t, max_t, avg_t = compute_temperature_stats(temps)
        alerts = count_above_threshold(temps, alert_threshold)
        overall_readings.extend(temps)
        print(
            f"{station:16s} | Min: {min_t:5.2f} C | Max: {max_t:5.2f} C | "
            f"Avg: {avg_t:5.2f} C | Days > {alert_threshold}C: {alerts}"
        )

    o_min, o_max, o_avg = compute_temperature_stats(overall_readings)
    print("-" * 72)
    print(f"Overall Summary  | Min: {o_min:5.2f} C | Max: {o_max:5.2f} C | Avg: {o_avg:5.2f} C")


if __name__ == "__main__":
    main()
