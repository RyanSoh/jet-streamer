#python flightsearch.py
from collections import deque
import heapq
from destinations import all_destinations

def bfs_flight_search(start, end, destinations, max_stops):
    queue = [(0, start, [start])]  # (total cost, current airport, path taken)
    itineraries = []

    while queue:
        cost, current, path = heapq.heappop(queue)

        if current == end:
            itineraries.append((path, cost))
            max_stops = min(max_stops, len(path)+2)
            continue

        if len(path) - 2 >= max_stops: 
            continue

        # forward direction
        next_destinations = destinations.get(current, {})
        for next_dest, next_cost in next_destinations.items():
            if next_dest not in path:
                heapq.heappush(queue, (cost + next_cost, next_dest, path + [next_dest]))

        # reverse direction
        for prev_dest, connections in destinations.items():
            if current in connections and prev_dest not in path:
                heapq.heappush(queue, (cost + connections[current], prev_dest, path + [prev_dest]))

    return itineraries

def calculate_price(itinerary, base_cost, optimal_stops):
    stops = len(itinerary) - 2
    if 'CAI' not in itinerary and stops != 0:
        base_cost += 100
    if stops <= optimal_stops:
        return base_cost - 150 * stops
    else:
        return base_cost - 150 * optimal_stops + 200 * (stops - optimal_stops)

def search_flights(start, end, destinations, max_stops):
    itineraries_outbound = bfs_flight_search(start, end, destinations, max_stops)

    if not itineraries_outbound:
        return []

    min_stops_outbound = min(len(itinerary[0]) for itinerary in itineraries_outbound) - 2

    results = []

    for itinerary, cost in itineraries_outbound:
        stops = len(itinerary) - 2
        if stops <= min_stops_outbound + 2: 
            price = calculate_price(itinerary, cost, min_stops_outbound)
            results.append((itinerary, price))

    return results

def main():
    o = input("Input origin airport code: ")
    d = input("Input destination code: ")
    if o==d:
        return
    max_stops = 3
    results = search_flights(o, d, all_destinations, max_stops)

    results.sort(key=lambda x: x[1])

    if results:
        min_price = results[0][1]

        filtered_results = [result for result in results if result[1] <= 2 * min_price]

        for i, (itinerary, price) in enumerate(filtered_results[:5]):
            print(f"Route: {' -> '.join(itinerary)}, Price: ${round(price / 6)}")

if __name__ == "__main__":
    main()