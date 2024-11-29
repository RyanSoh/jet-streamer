from flask import Flask, render_template, request
from flightsearch import search_flights 
from destinations import all_destinations
from howmany import numdest, numhubs 
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        origin = request.form["origin"]
        destination = request.form["destination"]
        max_stops = 3

        if origin != destination:
            results = search_flights(origin, destination, all_destinations, max_stops)
        else:
            results = []

        # Sort the results based on price
        results.sort(key=lambda x: x[1])

        # Initialize filtered results
        filtered_results = []

        if results:
            # Determine the minimum price
            min_price = results[0][1]

            # Filter results based on the condition
            filtered_results = [
                {"itinerary": " -> ".join(itinerary), "price": round(price / 6)}
                for itinerary, price in results
                if price <= 2 * min_price
            ]

            # Limit to the top 5 results
            filtered_results = filtered_results[:5]

        # Render the template with filtered results
        return render_template("index.html", results=filtered_results)

    # If GET request, show empty form
    return render_template("index.html", results=None)


@app.route("/about")
def about():
    # Call the functions to get the number of hubs and destinations
    hubs = numhubs(all_destinations)  # Get the number of hubs
    destinations = numdest(all_destinations)  # Get the number of unique destinations

    # Pass the values to the template
    return render_template("about.html", hubs=hubs, destinations=destinations)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


