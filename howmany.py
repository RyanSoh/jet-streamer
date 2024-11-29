from destinations import all_destinations

def numdest(all_destinations):
  # Initialize an empty set to store unique airport codes
  unique_airports = set()
  
  # Iterate through the dictionary and add all the airport codes to the set
  for destinations in all_destinations.values():
      unique_airports.update(destinations.keys())
  
  # The number of unique airport codes is the size of the set
  num_unique_airports = len(unique_airports)
  return num_unique_airports

def numhubs(all_destinations):
  return len(all_destinations.keys())