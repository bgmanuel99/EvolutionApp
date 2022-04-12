import os
import datetime

class ReportsLogGenerator():

    """This class generates all the report logs for the application"""

    def __init__(self):
        pass

    @staticmethod
    def initilize_evolution_report_log(reports_path="", data=None, time_of_creation=None):
        """This method initilize the evolution report log"""

        evolution_report_log = open(reports_path, "w")

        evolution_report_log.write("------------------------\n")
        evolution_report_log.write("| EVOLUTION REPORT LOG |\n")
        evolution_report_log.write("------------------------\n")
        evolution_report_log.write("\nCreated at: {}:{}:{} {}/{}/{}\n".format(
            time_of_creation[0],
            time_of_creation[1],
            time_of_creation[2],
            time_of_creation[3],
            time_of_creation[4],
            time_of_creation[5]
        ))
        evolution_report_log.write("\n- Initial data:\n")
        evolution_report_log.write("    Number of individuals -> {}\n".format(data[0]))
        evolution_report_log.write("    Number of food -> {}\n".format(data[1]))
        evolution_report_log.write("    Number of epochs -> {}\n".format(data[2]))

        evolution_report_log.close()

    @staticmethod
    def write_evolution_data_to_log(reports_path="", data=None, running_state=""):
        """This method inserts data into the evolution report log"""

        evolution_report_log = open(reports_path, "a")

        if running_state == "initializing_epoch":
            # Write the initial data of an epoch into the evolution report log
            first_message = "\nEPOCH {} INITIAL DATA\n".format(data["actual_epoch"])
            evolution_report_log.write(first_message)
            first_message_underlining = "-" * len(first_message)
            evolution_report_log.write(first_message_underlining)
            evolution_report_log.write("\n")
            evolution_report_log.write("Number of individuals -> {}\n".format(data["number_of_individuals"]))
            evolution_report_log.write("Number of food -> {}\n".format(data["number_of_food"]))
            evolution_report_log.write("Number of non survival individuals -> {}\n".format(data["number_of_non_survival_individuals"]))
            evolution_report_log.write("Number of survival individuals -> {}\n".format(data["number_of_survival_individuals"]))
            evolution_report_log.write("Number of evolving individuals -> {}\n".format(data["number_of_evolving_individuals"]))
            evolution_report_log.write("Maximum number of individuals -> {}\n".format(data["maximum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of individuals -> {}\n".format(data["minimum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of food -> {}\n".format(data["minimum_number_of_food"]))
            evolution_report_log.write("Maximum velocity of an individual -> {}\n".format(data["maximum_velocity_of_an_individual"]))
            evolution_report_log.write("Minimum velocity of an individual -> {}\n".format(data["minimum_velocity_of_an_individual"]))
            evolution_report_log.write("Maximum size of an individual -> {}\n".format(data["maximum_size_of_an_individual"]))
            evolution_report_log.write("Minimum size of an individual -> {}\n".format(data["minimum_size_of_an_individual"]))
            evolution_report_log.write("Most appearing velocity (velocity, individuals) -> [{}, {}]\n".format(data["most_appearing_velocity"][0], data["most_appearing_velocity"][1]))
            evolution_report_log.write("Most appearing size (size, individuals) -> [{}, {}]\n".format(data["most_appearing_size"][0], data["most_appearing_size"][1]))

            # Write the header of the running state of the evolution report for an epoch, so it is only write once
            first_message = "\nRUNNING EPOCH {} DATA\n".format(data["actual_epoch"])
            evolution_report_log.write(first_message)
            first_message_underlining = "-" * len(first_message)
            evolution_report_log.write(first_message_underlining)
            evolution_report_log.write("\n")
        elif running_state == "running_epoch":
            # Write data of the epoch while it is running
            if len(data) == 1:
                evolution_report_log.write("Number of non survival individuals got down to-> {}\n".format(data[0]))
            else:
                if data[0] != None: evolution_report_log.write("Number of survival individuals got up to-> {}\n".format(data[0]))
                if data[1] != None: evolution_report_log.write("Number of evolving individuals got up to-> {}\n".format(data[1]))
        elif running_state == "ending_epoch":
            # Write the ending data of an epoch into the evolution report log
            first_message = "\nEPOCH {} FINAL DATA\n".format(data["actual_epoch"])
            evolution_report_log.write(first_message)
            first_message_underlining = "-" * len(first_message)
            evolution_report_log.write(first_message_underlining)
            evolution_report_log.write("\n")
            evolution_report_log.write("Number of individuals -> {}\n".format(data["number_of_individuals"]))
            evolution_report_log.write("Number of food -> {}\n".format(data["number_of_food"]))
            evolution_report_log.write("Number of non survival individuals -> {}\n".format(data["number_of_non_survival_individuals"]))
            evolution_report_log.write("Number of survival individuals -> {}\n".format(data["number_of_survival_individuals"]))
            evolution_report_log.write("Number of evolving individuals -> {}\n".format(data["number_of_evolving_individuals"]))
            evolution_report_log.write("Maximum number of individuals -> {}\n".format(data["maximum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of individuals -> {}\n".format(data["minimum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of food -> {}\n".format(data["minimum_number_of_food"]))
            evolution_report_log.write("Maximum velocity of an individual -> {}\n".format(data["maximum_velocity_of_an_individual"]))
            evolution_report_log.write("Minimum velocity of an individual -> {}\n".format(data["minimum_velocity_of_an_individual"]))
            evolution_report_log.write("Maximum size of an individual -> {}\n".format(data["maximum_size_of_an_individual"]))
            evolution_report_log.write("Minimum size of an individual -> {}\n".format(data["minimum_size_of_an_individual"]))
            evolution_report_log.write("Most appearing velocity (velocity, individuals) -> [{}, {}]\n".format(data["most_appearing_velocity"][0], data["most_appearing_velocity"][1]))
            evolution_report_log.write("Most appearing size (size, individuals) -> [{}, {}]\n".format(data["most_appearing_size"][0], data["most_appearing_size"][1]))
            evolution_report_log.write("Epoch execution time -> {} seconds\n".format(data["epoch_time"]))
        elif running_state == "ending_algorithm":
            # Write the ending data of the algorithm, which means the last epoch data that has been processed by the genetic algorithm
            first_message = "\nALGORITHM FINAL DATA\n"
            evolution_report_log.write(first_message)
            first_message_underlining = "-" * len(first_message)
            evolution_report_log.write(first_message_underlining)
            evolution_report_log.write("\n")
            evolution_report_log.write("Number of individuals -> {}\n".format(data["number_of_individuals"]))
            evolution_report_log.write("Number of food -> {}\n".format(data["number_of_food"]))
            evolution_report_log.write("Number of non survival individuals -> {}\n".format(data["number_of_non_survival_individuals"]))
            evolution_report_log.write("Number of survival individuals -> {}\n".format(data["number_of_survival_individuals"]))
            evolution_report_log.write("Number of evolving individuals -> {}\n".format(data["number_of_evolving_individuals"]))
            evolution_report_log.write("Maximum number of individuals -> {}\n".format(data["maximum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of individuals -> {}\n".format(data["minimum_number_of_individuals"]))
            evolution_report_log.write("Minimum number of food -> {}\n".format(data["minimum_number_of_food"]))
            evolution_report_log.write("Maximum velocity of an individual -> {}\n".format(data["maximum_velocity_of_an_individual"]))
            evolution_report_log.write("Minimum velocity of an individual -> {}\n".format(data["minimum_velocity_of_an_individual"]))
            evolution_report_log.write("Maximum size of an individual -> {}\n".format(data["maximum_size_of_an_individual"]))
            evolution_report_log.write("Minimum size of an individual -> {}\n".format(data["minimum_size_of_an_individual"]))
            evolution_report_log.write("Most appearing velocity (velocity, individuals) -> [{}, {}]\n".format(data["most_appearing_velocity"][0], data["most_appearing_velocity"][1]))
            evolution_report_log.write("Most appearing size (size, individuals) -> [{}, {}]\n".format(data["most_appearing_size"][0], data["most_appearing_size"][1]))
        elif running_state == "finish_report_data":
            # Write the last epoch of the algorithm and the time of the algorithm's execution
            evolution_report_log.write("\nThe algorithm finished at epoch {}\n".format(data[0]))
            evolution_report_log.write("The algorithm took {} {} to run".format(data[1][0], data[1][1]))

        evolution_report_log.close()

    @staticmethod
    def write_message_to_evolution_log(reports_path="", message=""):
        """This method writes messages to the evolution report log"""

        evolution_report_log = open(reports_path, "a")

        evolution_report_log.write("\n{}\n".format(message))

        evolution_report_log.close()

    @staticmethod
    def write_error_data_to_log(type="", message=""):
        """This method inserts errors, warnings or any other util information to the errors report log"""

        errors_report_log = open(os.getcwd().replace("\\", "/") + "/log/error/errors_log.txt", "a")

        actual_time_of_error = datetime.datetime.now()

        errors_report_log.write("{}/{}/{} {}:{}:{} [{}] {}\n".format(
            actual_time_of_error.strftime("%d"),
            actual_time_of_error.strftime("%m"),
            actual_time_of_error.strftime("%Y"),
            actual_time_of_error.strftime("%H"),
            actual_time_of_error.strftime("%M"),
            actual_time_of_error.strftime("%S"),
            type.upper(),
            message
        ))

        errors_report_log.close()

    @staticmethod
    def delete_errors_report_log_content():
        """This method deletes all the data on the errors report log"""

        open(os.getcwd().replace("\\", "/") + "/log/error/errors_log.txt", "w").close()