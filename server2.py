import time

import QuestionC

print(" ")
print("server2: creating cache sever")
# From the library, initialize our class to record the cache
# The initialization also make the cache system start listening on the server and allow for 10 clients connection (other cache servers in this case)
server_cache = QuestionC.server_cache(5, [('10.0.0.134', 83)], 84, 10)
print(" ")


def very_expensive_read_from_disk():
    print("expensive function called from server2")
    return "Pretend this string have to be read from disk and is very expensive to do so"


def get_string():
    lookup = None
    if "get_string" in server_cache.dic:
        lookup = server_cache.find_cache(server_cache.dic["get_string"])
    # If not cached
    if not lookup:
        lookup = very_expensive_read_from_disk()
    # Update the cache and get the id of the object that this function return
    # Programmer using the library is responsible for putting in the right function name
    server_cache.add_cache(lookup, "get_string")
    return lookup


# Let set up a while loop which act as server running online and listening for input
# The input can be acquired from file. We can change the Server2.txt to specify the input. The valid input are:
# get_string - call the get_string function on the server
# wait - Have this server idle for 20 seconds
# exit - shut down this server
# everything else - prompt the message saying that it is an invalid input and proceed with listening for new input
# If want to test this server manually, please delete Server1.txt file. The program will ask you for the input
f = None
try:
    f = open('Server2.txt')
except FileNotFoundError:
    pass
i = 0
while True:
    txt = "Some random text"
    if f:
        print("server2: input file detected. Reading from Server2.txt")
        txt = f.readline()
        txt = txt.strip()
    else:
        txt = input("server2: Please enter get_string, exit or wait: ")
    print(" ")
    if txt == "exit":
        print("server2: Got exited. Shutting down server2")
        break
    elif txt == "get_string":
        get_string()
        i = i + 1
        if i == 1:
            print("server2: get_string function called\nYou called get_string function " +
                  str(i) +
                  " times now.\n" +
                  "However, You should NOT see 'expensive function called from serverxxx' above becuase it is called once on other server!!")
            print(' ')
            time.sleep(2)
        else:
            print("server2: get_string function called\nYou called get_string function " +
                  str(i) +
                  " times now.\n" +
                  "You should NOT see 'expensive function called from serverxxx' above")
            print(' ')
            time.sleep(2)
    elif txt == "wait":
        print("server2: Got wait. Idling for 20 second")
        print(' ')
        time.sleep(20)
    else:
        print("Server2: Input not recognized. Please enter get_string, exit, or wait when prompted next\n" +
              "The valid inputs are:\n" +
              "get_string - call the get_string function on the server\n" +
              "wait - Have this server idle for 20 seconds\n" +
              "exit - shut down this server")
        print(' ')
        time.sleep(2)

if f:
    f.close()

# Stop the cache server
server_cache.stop_listen()
