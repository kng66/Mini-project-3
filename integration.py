""" IntegrationProcessor module """
import json
from config import Config


class IntegrationProcessor():
    """ This class manages other processors into one integration pipeline. """

    def __init__(self, root_path, output_path):
        self.root_path = root_path
        self.output_path = output_path

    def integrate(self):
        """ Main integrating function. Binds FileProcessor and ConfigProcessor together.
        First, an array of patients is being made based on what is inside the folder under the given path.
        Then, the ConfigProcessor parses the template from the given path and renders the output. """
        # Generating result based on the config file
        print("Reading the template file...")
        result = Config(self.root_path).render_template()
        # Writing the result to the output file
        print("Saving the output file...")
        self.save_to_file(result)
        # Sending a request to FHIR backend (if applicable)

    def save_to_file(self, string):
        """ Saves given string to a file. """
        with open(self.output_path, "w") as text_file:
            json.dump(string, text_file, indent=4)
            print("\033[92mSaved to file \033[0m" + self.output_path)
