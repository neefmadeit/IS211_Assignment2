import argparse
import logging
import sys


# Assume the following functions are defined elsewhere in your script:
# def downloadData(url):
#     """Downloads data from a URL and returns it as a string."""
#     # ... implementation ...
#     pass
#
# def processData(data):
#     """Processes CSV data string into a dictionary of person tuples."""
#     # ... implementation ...
#     pass
#
# def displayPerson(person_id, person_data):
#     """Looks up a person by ID and prints their details."""
#     # ... implementation ...
#     pass

def setup_logger():
    """Configures the 'assignment2' logger to write to 'errors.log'."""
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)  # Set to catch ERROR level and above

    file_handler = logging.FileHandler('errors.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger


def main():
    """Main function to run the script logic."""
    # 1. Use argparse for the URL parameter
    parser = argparse.ArgumentParser(description="Download and process data from a URL.")
    parser.add_argument('url', type=str, help="The URL to download data from (required).")
    args = parser.parse_args()

    # The 'url' is required; argparse handles the case where it's missing by
    # printing an error and exiting automatically because it's a positional argument.

    # Setup the logger
    logger = setup_logger()

    # 2. Call downloadData() with exception handling
    try:
        # Assuming downloadData function is available
        # from your_module_name import downloadData
        csvData = downloadData(args.url)
    except Exception as e:
        error_message = f"An error occurred during data download: {e}"
        print(error_message, file=sys.stderr)
        logger.error(error_message)
        sys.exit(1)  # Exit the program on failure

    # 3. Logger is set up by setup_logger()

    # 4. Call processData()
    try:
        # Assuming processData function is available
        # from your_module_name import processData
        personData = processData(csvData)
    except Exception as e:
        error_message = f"An error occurred during data processing: {e}"
        print(error_message, file=sys.stderr)
        logger.error(error_message)
        sys.exit(1)  # Exit the program on failure

    # 5. Ask the user for an ID to lookup
    while True:
        user_input = input("Enter an ID to look up (or a negative number/0 to exit): ")
        try:
            person_id = int(user_input)
            if person_id <= 0:
                print("Exiting program.")
                break
            else:
                # Assuming displayPerson function is available
                # from your_module_name import displayPerson
                displayPerson(person_id, personData)
        except ValueError:
            print(f"Invalid input: '{user_input}'. Please enter a valid integer ID.")
        except Exception as e:
            # Catch exceptions that might occur within displayPerson (e.g., ID not found)
            error_message = f"An unexpected error occurred while displaying person: {e}"
            print(error_message, file=sys.stderr)
            logger.error(error_message)
            # Continue the loop after an error in display


if __name__ == "__main__":
    # Placeholder functions to allow the code to run for demonstration
    def downloadData(url):
        print(f"Downloading from {url} (Simulated success)")
        return "id,name,age\n1,Alice,30\n2,Bob,25\n3,Charlie,35"


    def processData(data):
        print("Processing data (Simulated success)")
        lines = data.strip().split('\n')[1:]
        person_dict = {}
        for line in lines:
            try:
                p_id, name, age = line.split(',')
                person_dict[int(p_id)] = (name, int(age))
            except ValueError:
                continue
        return person_dict


    def displayPerson(person_id, person_data):
        person = person_data.get(person_id)
        if person:
            print(f"ID {person_id}: Name: {person[0]}, Age: {person[1]}")
        else:
            raise ValueError(f"ID {person_id} not found.")


    main()
