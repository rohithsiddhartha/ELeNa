# Elevation-Based Navigation (ELeNA)
## by Indentation&Semicolons
Elevation-based Navigation (EleNa) is an application that, given a start and end location, computes a route that maximizes or minimizes the elevation gain and limits the total distance between the locations to x% of the shortest path.

# Steps to run:

## Setting up the Virtual environment

### Linux
sudo apt-get install python3-venv    # If needed

python3 -m venv .venv

source .venv/bin/activate

### macOS
python3 -m venv .venv

source .venv/bin/activate

export FLASK_ENV=development
export FLASK_APP=src/App.py

### Windows
python3 -m venv .venv

.venv\scripts\activate

set FLASK_ENV=development
set FLASK_APP=src/App.py


## Install dependencies / requirements using the command
* pip3 install -r requirements.txt

## Running the application
* flask run 

## Testing the application (unit test cases)
* python3 test/test.py

## Using the application
* Head over to http://127.0.0.1:5000/ to use the web interface
* User enters the start location, end location, Maximum percentage deviation from shortest path and Elevation Preference
* Clicking on the Calculate button shows the Total distance, Elevation gain, elevation path along with the directions
* User can reset the input parameters by clicking the reset button
