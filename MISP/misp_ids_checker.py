import urllib3
import argparse
import logging
from pymisp import PyMISP, MISPAttribute
from datetime import datetime, timedelta

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("misp_script.log"),
        logging.StreamHandler()
    ]
)

# Variables
misp_url = "https://localhost"
api_key = "KI8oZgPfZmdIkARYB4mEP0in7dr6empSVyAYGVdS"
misp_verifycert = False

# Initialize MISP client
misp = PyMISP(misp_url, api_key, misp_verifycert)

# Calculate datefrom based on --last argument
def calculate_timestamp(last_days):
    try:
        days = int(last_days[:-1])
        if last_days.endswith("d"):
            timestamp = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            return timestamp
        else:
            raise ValueError("Invalid format. Use 'Xd', for example '1d' or '365d'.")
    except Exception as e:
        logging.error(f"Error calculating timestamp: {e}")
        return None


# Fetch events with optional date filtering
def fetch_events(date_filter=None):
    search_params = {
        "returnFormat": "json",
        "published": 0,
        "publish_timestamp": 0,
    }

    # Use last for date and timestamp for last modified date
    if date_filter:
        search_params["timestamp"] = date_filter

    try:
        logging.info(f"Fetching events with parameters: {search_params}")
        events = misp.search("events", **search_params)
        logging.info(f"Found {len(events)} events to process.")
        return events
    except Exception as e:
        logging.error(f"Failed to fetch events: {e}")
        return []

# Process attributes in events
def process_event_attributes(events):
    for event in events:
        event_id = event['Event']['id']
        logging.info(f"Processing Event ID: {event_id}")

        try:
            # Fetch attributes for the event
            event_data = misp.get_event(event_id)
            attributes = event_data['Event']['Attribute']

            for attribute in attributes:
                logging.debug(f"Processing Attribute: {attribute.get('value')}")

                # Extract necessary fields
                attribute_id = attribute.get('id')
                if attribute.get('to_ids') and attribute.get('warnings'):
                    # Recreate the attribute and change the IDS flag
                    misp_attr = MISPAttribute()
                    misp_attr.from_dict(**attribute)
                    misp_attr.to_ids = False

                    # Push the updated attribute
                    try:
                        misp.update_attribute(misp_attr, attribute_id)
                        logging.info(f"Updated Attribute ID {attribute_id} - IDS flag removed")
                    except Exception as e:
                        logging.error(f"Failed to update Attribute ID {attribute_id}: {e}")

        except Exception as e:
            logging.error(f"Failed to process Event ID {event_id}: {e}")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Process MISP events and attributes.")
    parser.add_argument("--last", help="Filter events by the last X days (e.g., '1d', '30d').", default=None)
    args = parser.parse_args()

    # Convert --last arg to timestamp
    date_filter = calculate_timestamp(args.last)
    if not date_filter:
        logging.error("Invalid '--last' argument format. Use 'Xd' for example '1d' or '365d'. Exiting")
        exit(1)

    logging.info(f"Script started at {datetime.now()} with date filter: {date_filter}")

    # Fetch and process events
    events = fetch_events(date_filter)
    process_event_attributes(events)

    logging.info(f"Script finished at {datetime.now()}")
