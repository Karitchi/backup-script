import argparse
import os
import zipfile
import datetime


def parse_args():
    """Parse the command line arguments.

    The following arguments are accepted:
    - source: the file or directory to be backed up (required)
    - destination: the file to save the backup to (required)
    - --name: the optional name of the backup file

    Returns:
        argparse.Namespace: an object containing the parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source", nargs="+", help="the file or directory to be backed up")
    parser.add_argument("destination", help="the file to save the backup to")
    parser.add_argument("--name", help="the name of the .zip file")
    return parser.parse_args()


def get_current_time():
    """Get the current time and format it as a string in the desired format.

    Returns:
        str: the current time formatted as a string in the format "dd-mm-yy_hh-mm-ss"
    """

    # Get the current time
    now = datetime.datetime.now()

    # Format the current time as a string in the desired format
    current_time = now.strftime("%d-%m-%y_%H-%M-%S")

    return current_time


def create_zip_filepath(current_time, destination, name):
    """Create the complete file path for the zip file.

    Args:
        current_time (str): the current time formatted as a string in the format "dd-mm-yy_hh-mm-ss"
        destination (str): the file path to save the backup zip file to
        name (str): the optional name of the backup file

    Returns:
        str: the complete file path for the zip file
    """

    # create zip file name
    if name == None:
        zip_name = f"backup_{current_time}.zip"
    else:
        zip_name = f"{name}.zip"

    # create zip file complete path
    zip_filepath = f"{destination}/{zip_name}"
    return zip_filepath


def create_zip_file(zip_filepath, sources):
    """Compress the source file or files and all their contents into a .zip file and store it in the destination location.

    Args:
        zip_filepath (str): the file path to save the zip file to
        sources (list): a list of file or directory paths to be backed up

    Returns:
        None
    """

    # Create a ZipFile object
    zip_obj = zipfile.ZipFile(zip_filepath, 'w')

    # Iterate over the sources
    for source in sources:
        # Walk through the source directory and add all the files to the zip file
        for root, dirs, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                zip_obj.write(file_path)

    # Close the ZipFile object and write the zip file to the filesystem
    zip_obj.close()


def print_finish_message(sources, destination, zip_filepath):
    """
    Print a message indicating that the backup of the given sources has been completed and saved to the given destination.

    Parameters:
    - sources: a list of strings representing the sources that were backed up.
    - destination: a string representing the file path of the destination where the backup was saved.

    Returns:
    - None. This function prints the message to the standard output and does not return anything.
    """

    # Print a message to indicate that the backup is finished
    num_sources = len(sources)
    size = os.path.getsize(zip_filepath) / (1024 * 1024)
    print(
        f"The backup of {num_sources} sources has been completed and saved to {destination} (size: {size:.2f} MB).")


def zipources(sources, destination, name):
    """Compress the source file or files and all their contents into a .zip file and store it in the destination location.

    Args:
        sources (list): a list of file or directory paths to be backed up
        destination (str): the file path to save the backup zip file to

    Returns:
        None
    """

    # get the formated current time
    current_time = get_current_time()
    # create the complete filepath of the backup file
    zip_filepath = create_zip_filepath(current_time, destination, name)
    # create the backup file itself
    create_zip_file(zip_filepath, sources)
    # print a message when the backup is done
    print_finish_message(sources, destination, zip_filepath)


def main():
    # parse the command-line arguments
    args = parse_args()

    # get the sources and destination from the parsed arguments
    sources = args.source
    destination = args.destination
    name = args.name

    # creates the backup folder if it does not exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Zip the sources and save the zip file to the destination
    zip_sources(sources, destination, name)


if __name__ == "__main__":
    main()
