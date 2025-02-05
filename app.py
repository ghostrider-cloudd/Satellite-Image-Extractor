from flask import Flask, render_template, request
import requests
import os

# Initialize Flask app
app = Flask(__name__)

# Define folder to store images
IMAGE_FOLDER = "static"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Replace with your actual Google Maps API Key
GOOGLE_API_KEY = "Replace with your actual Google Maps API Key"

def get_satellite_image(lat, lon, zoom):
    """
    Fetches a satellite image from Google Static Maps API.
    
    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        zoom (int): Zoom level (1-21).
    
    Returns:
        str: Path to the saved image if successful, None otherwise.
    """
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size=600x300&maptype=satellite&key={GOOGLE_API_KEY}"
    
    
    response = requests.get(url)
    
    if response.status_code == 200:
        # Define file path for saving the image
        image_path = f"{IMAGE_FOLDER}/satellite_{lat}_{lon}_zoom{zoom}.jpg"
        
        # Save image file locally
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        return image_path  # Return saved image path
    return None  # Return None if request failed

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main web interface.

    - If method is GET: Renders the form for input.
    - If method is POST: Takes user input, fetches the satellite image, and displays it.

    Returns:
        HTML page (index.html) with form and image.
    """
    if request.method == "POST":
        # Get user inputs from the form
        lat = request.form.get("latitude")
        lon = request.form.get("longitude")
        zoom = request.form.get("zoom")

        try:
            # Convert inputs to appropriate data types
            lat, lon, zoom = float(lat), float(lon), int(zoom)

            # Validate zoom level (must be between 1 and 21)
            if zoom < 1 or zoom > 21:
                return render_template("index.html", error="Zoom level must be between 1 and 21.")
        except ValueError:
            return render_template("index.html", error="Invalid input! Please enter valid numbers.")

        # Fetch satellite image
        image_path = get_satellite_image(lat, lon, zoom)

        if image_path:
            return render_template("index.html", image_url=image_path)

        return render_template("index.html", error="Failed to retrieve image.")

    return render_template("index.html")  # Render form page initially

if __name__ == "__main__":
    app.run(debug=True)  # Start Flask server
