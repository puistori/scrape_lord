"""
This file contains code used to scrape all the data from a list of URLS.

You must give it the following:
 1. the scraping function that you are using. You'll have to design this yourself, of course.
    !!!The scraping function must have two parameters (unless you want to change the source code here).
    !! The two parameters must be named URL (for the URL you're trying to scrape from) and requester (in
    order to reference the requester object)
    ## fix with kwargs?
 2. The name of the file containing the scraping assignment.
    The scraping assignment must be a pickled list.
 3. Options and parameters for the Safe_Request object
    This means 'times' 'timeout' and 'proxy_timeout'  which respectively manage how many iterations are used
    with the same proxy, how long you'll wait for a request to resolve, and how long you'll wait on a proxy to respond before
    skipping to another one.
4. outputname. this will govern the name of your output, as well as your error logs.
    The output name should NOT have any file extensions in it (don't say .txt, we'll take care of that)
5. writing options; choose whether the output will be text or bites (pickling), and
   whether you are overwriting or appending to that file or object. write "wt" or "wb" for
   writing text or writing bytes ( and then pickling ) respectively. By default, write_type
   is set to "wt" and append is set to True.
   !!! If you are appending to a pickled object, the pickled object must be a string, list or dictionary.
6. assignment_type - is the assignment a text file or is it a list stored in bytes? 'rt' and 'rb' are the arguments you want.


!!! Also, a word to the wise - for the emergency save feature to work, you probably need to run this from a command line
like the bash command line. That's because they signal that an IDE like mine (pycharm) gives is uncatchable.

"""

import Safe_Request
import time_parser
import pickle
import time
import os.path
import warnings
import signal
import sys


#update number at three places.


# Using this code to redirect warning to stdout

def myWarning(message, category, filename, lineno, file=None, line=None):
    sys.stdout.write(warnings.formatwarning(message, category, filename, lineno))

warnings.showwarning = myWarning



def sweep(scrape_function,scraping_assignment,output_name,times=50,timeout=20,proxy_timeout=5,
          write_type="wt",append=True,delim="\n",sleep_time=1,verify=True,assignment_type='rt'):

    sys.stdout.write("Starting sweep up!")
    sys.stdout.write("\n")
    sys.stdout.flush()
    # Dealing with overwrite/append issues.
    if append == True:
        if os.path.exists(output_name) and os.path.isfile(output_name):
            test = open("%s"%output_name,'rb')
            testP = pickle.load(test)
            test.close()
            if type(testP) != str and type(testP) != list:
                warnings.warn("\033[1;31;47m Invalid append type. The script will instead REPLACE any file with the name %s \033[10;39;49m \n"%output_name)
                append = False

        else:
            warnings.warn("")
            warnings.warn("\033[1;31;47m Sorry, the file you wanted to overwrite could not be found. Creating one from scratch. \033[10;39;49m \n")
            append = False


    # opening error log
    error_log_name = output_name +"_error_log.txt"
    log = open('%s'%error_log_name,'a')
    log.write("This file contains the error messages\nfor a new scraping session.\n")
    log.close()

    # opening a success_log
    success_log_name = output_name+"_success_log.txt"
    success_log = open("%s"%success_log_name, 'a')
    success_log.write("This file contains the successfully scraped scraping assignments for a new scraping session.")
    # I don't have the same motivation to close this log, so I'll keep it open.


    # Creating Safe_Requester object
    requester = Safe_Request.Safe_Requester(times=times,timeout=timeout,proxy_timeout=proxy_timeout,
                                            error_log_name=error_log_name,verify=verify)

    #Loading in scraping assignment
    if assignment_type == 'rt':
        load_in = open(scraping_assignment,encoding='utf8')
        scraping_assignment = load_in.read().splitlines()
        load_in.close()
    else:
        pickle_in = open('%s'%scraping_assignment, 'rb')
        scraping_assignment = pickle.load(pickle_in)
        pickle_in.close()

    # Everything gets stored in a big list.
    Sweep_results = []

    # We want these to be saved in case we have to interrupt our program for whatever reason.

    def keyboardInterruptHandler(signal, frame):
        emergency_save = open("%s_emergency_save"%output_name, 'wb')
        pickle.dump(Sweep_results,emergency_save)
        emergency_save.close()
        success_log.close()
        exit(-1)

    signal.signal(signal.SIGINT, keyboardInterruptHandler)



    # We're all set! Now the actual scraping begins.
    assignment_length = len(scraping_assignment)
    count = 0
    start_time = time.time()
    for assignment in scraping_assignment:

        # Giving a progress report first. How far along are we?
        try:
            percent_completed = str ( (count / assignment_length) * 100 )
            
            time_spent = time.time() - start_time
            if percent_completed > 0:

                hr1, min1, sec1 = time_parser.parse_time(time_spent)
                hr2,min2,sec2 = time_parser.parse_time((time_spent/percent_completed)-time_spent)
                sys.stdout.write(("%s percent of the way done ; %s down and %s to go. "
                        "\n  You have spent %s hours, %s minutes and %s seconds scraping. "
                        "\n At this rate, you will be done in %s hours, %s minutes and %s seconds."
                        " "%(percent_completed,count,(assignment_length-count),hr1,min1,sec1,hr2,min2,sec2)))
                sys.stdout.write("\n")
                sys.stdout.flush()
            else:
                sys.stdout.write("You've just begun. %s down and %s to go."%(count,(assignment_length-count)))
                sys.stdout.write("\n")
                sys.stdout.flush()
        except Exception as e:
            sys.stdout.write("something went wrong while reporting the progress.")
            import traceback
            print(traceback.format_exception_only(type(e), e)[0])

            sys.stdout.write("\n")
            sys.stdout.flush()

        time.sleep(sleep_time)
        count += 1
        try:
            data = scrape_function(URL=assignment,requester=requester)
            Sweep_results.append(data)
            success_log.write(str(assignment)+"\n")

        except Exception as e:
            # This may be inefficient, but I'm concerned because the subfunction sameuses the log :/
            log = open('%s' % error_log_name, 'a')
            Error = ("Error with href %s" % scraping_assignment) + " : " + str(e) + "\n"
            log.write(Error)
            log.close()


    # saving our data! This will depend on our saving options. I set the encoding to utf8
    success_log.close()
    if write_type =="wt":
        appendingOrWriting = "a"
        if append == False:
            appendingOrWriting = "wt"
        results = open("%s.txt"%output_name,appendingOrWriting,encoding='utf8')
        for datapoint in Sweep_results:
            results.write(str(datapoint)+delim)
        results.close()
    elif write_type == "wb":

        if append == True:
            pickle_in = open("%s"%output_name,'rb',encoding='utf8')
            old_data = pickle.load(pickle_in)

            if type(old_data == str):
                for datapoint in Sweep_results:
                    old_data += datapoint
                    old_data += delim
            if type(old_data == list):
                for datapoint in Sweep_results:
                    old_data.append(datapoint)
            pickle_in.close()

            pickle_out = open("%s"%output_name,'wb')
            pickle.dump(old_data,pickle_out)
            pickle_out.close()

        elif append == False:
            pickle_out = open('%s'%output_name,'wb')
            pickle.dump(Sweep_results,pickle_out)
            pickle_out.close()

