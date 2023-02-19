# Section 1
# Interpret Command Line
# file - file
# python c/cc cmd/file/console console/file -i input1.txt input2.txt -o output.txt
# file - console
# console - file
# console - console
# cmd - console
# cmd - file

import sys
import os
import shutil
import subprocess
import threading
import time
import multiprocessing
import signal


# Section 2
# Converting to single input output pattern
def input_output_patterns(input_pattern, output_pattern, additional_data):
    if input_pattern == "file" and output_pattern == "file":

        input_files_format = []
        output_files_format = []
        for data in additional_data:
            if data == "-i":
                temp_var = "i"
            elif data == "-o":
                temp_var = "o"
            elif data == "-f":
                temp_var = "f"
            elif temp_var == "i":
                input_files_format.append(data)
            elif temp_var == "o":
                output_files_format.append(data)

        current_dir_path = os.getcwd();
        current_input_dir_path = current_dir_path + "\Inputs"
        current_code_dir_path = current_dir_path + "\Codes"
        input_dir = os.listdir(current_input_dir_path)
        code_dir = os.listdir(current_code_dir_path)
        for input_00x in input_dir:

            # Set to add codes having compilation and run time errors

            compilation_error = {""}
            run_time_error = {""}

            # Picking a single code from Code Directory

            for code in code_dir:
                target_input_files_to_delete = []

                # Copying input file to the correct directory for run

                for input_file in os.listdir(current_input_dir_path + "\\" + input_00x):
                    original_input_file = current_input_dir_path + "\\" + input_00x + "\\" + input_file
                    if not os.path.isdir(original_input_file):
                        target_input_file = current_dir_path + "\\" + input_file
                        target_input_files_to_delete.append(target_input_file)
                        shutil.copyfile(original_input_file, target_input_file)

                # Copying code file to the correct directory for run

                original_code_file = current_code_dir_path + "\\" + code
                target_code_file = current_dir_path + "\\" + code
                shutil.copyfile(original_code_file, target_code_file)

                # Running Code

                # Edit: TO DO: TLE
                # Edit: TO DO: Compilation Error, DONE
                # Edit: TO DO: Run Time Error, DONE

                compilation = subprocess.call(["g++", code])

                # Checking for compilation errors

                if compilation != 0:
                    compilation_error.add(code)
                else:

                    # Attempt 1

                    # def run_code():
                    #     subprocess.call("./a.exe")
                    #
                    # thread_code_run = multiprocessing.Process(target=run_code,)
                    # thread_code_run.start()
                    # # To check for time limit exceed
                    # time.sleep(3)
                    # if thread_code_run.is_alive():
                    #     print("still running TLE")
                    #     thread_code_run.terminate()
                    # thread_code_run.join()

                    # Attempt 2

                    # def handler(signum, frame):
                    #     print("Forever is over!")
                    #     raise Exception("end of time")
                    #
                    # def run_code():
                    #     subprocess.call("./a.exe")
                    #
                    # signal.signal(signal.SIGALRM, handler)
                    #
                    # signal.alarm(3)
                    #
                    # try:
                    #     run_code()
                    # except Exception as exc:
                    #     print(exc)

                    # Checking for run time errors

                    run_error = subprocess.call("./a.exe")
                    if run_error != 0:
                        print("Run Time Error : Test Case " + input_00x + ", " + code)
                        run_time_error.add(code)
                    else:
                        # Removing temp files

                        os.remove(target_code_file)
                        for target in target_input_files_to_delete:
                            os.remove(target)
                        os.remove(current_dir_path + "/a.exe")

                        # Moving output files to input file folder

                        # Getting code name

                        temp = str(code).split(".")
                        code_name = temp[0]

                        path_directory = current_input_dir_path + "\\" + input_00x + "\\" + code_name
                        if not os.path.isdir(path_directory):
                            os.makedirs(path_directory, 0o755)

                        for output_file in output_files_format:
                            original_output_file = current_dir_path + "\\" + output_file
                            target_output_file = current_input_dir_path + "\\" + input_00x + "\\" + code_name + "\\" + output_file
                            shutil.copyfile(original_output_file, target_output_file)
                            os.remove(current_dir_path + "\\" + output_file)

            # Section 3
            # Processing Output files
            combined_output = []
            for output_file in output_files_format:
                single_output = []
                for code in code_dir:
                    if code not in run_time_error and code not in compilation_error:
                        for output_dir in os.listdir(
                                current_input_dir_path + "\\" + input_00x + "\\" + (code.split("."))[0]):
                            temp_address = current_input_dir_path + "\\" + input_00x + "\\" + (code.split("."))[
                                0] + "\\" + output_dir
                            f = open(temp_address, "r")
                            single_output.append(f.read())
                        combined_output.append(single_output)

            flag = True
            for output_file_number in combined_output:
                temp = output_file_number[0]
                for output in output_file_number:
                    if temp == output:
                        pass
                    else:
                        flag = False
            if flag != 0:
                print("Test Case " + input_00x + " Passed")
            else:
                print("Test Case " + input_00x + " Wrong Answer")

    return 1


def main(argv):
    language = sys.argv[1]
    input_format = sys.argv[2]
    output_format = sys.argv[3]
    additional_data = sys.argv[4:len(sys.argv)]
    type_io_pattern = input_output_patterns(input_format, output_format, additional_data)


if __name__ == "__main__":
    main(sys.argv[1:])
