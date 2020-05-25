Ormuco Challenge
===
This is the coding challenge as part of the hiring process for Ormuco Inc. The questions are the following:

Question A<br>
Your goal for this question is to write a program that accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap. As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).

Question B<br>
The goal of this question is to write a software library that accepts 2 version string as input and returns whether one is greater than, equal, or less than the other. As an example: “1.2” is greater than “1.1”. Please provide all test cases you could think of.

Question C<br>
At Ormuco, we want to optimize every bits of software we write. Your goal is to write a new library that can be integrated to the Ormuco stack. Dealing with network issues everyday, latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU (Least Recently Used) cache with time expiration. This library will be used extensively by many of our services so it needs to meet the following criteria:
1. Simplicity. Integration needs to be dead simple.
2. Resilient to network failures or crashes.
3. Near real time replication of data across Geolocation. Writes need to be in real time.
4. Data consistency across regions
5. Locality of reference, data should almost always be available from the closest region
6. Flexible Schema
7. Cache can expire

Please refer to the following sub-sections for each question specifically

Question A
---
The function implemented for this question is in QuestionA.py. The overlap function takes in two tuple each representing a line. The first element of the tuple is the starting point of the line and second is the end point of the line. They can also be reversed (first element is the end and second element is the start)!! The function return True if the two lines overlap or False otherwise.<br>

The test for this function is implemented in Ching_Chuan_Wu_test.py. The script reads in test case from QuestionA.txt. QuestionA.txt is in the format of the following:<br>
number_of_testcase<br>
start/end_of_first_line-----space-----start/end_of_first_line<br>
start/end_of_second_line-----space-----start/end_of_second_line<br>
True/False(1 for true, 0 for false)<br>
Repeat of the above three line<br>

The following is the test case in QuestionA.txt and their explanations:<br>
7 -------- There are seven test cases<br>
1 5 ------ First line starts at 1 and ends at 5<br>
2 6 ------ Second line starts at 2 and ends at 6<br>
1 -------- They overlap so return true<br>
5 1 ------ First line starts at 1 and ends at 1<br>
6 8 ------ Second line starts at 6 and ends at 8<br>
0 -------- They don't overlap so return False. This test case also cover case that the tuple is reversed<br>
2.3 4.4 -- First line starts at 2.3 and ends at 4.4 <br>
3 6.0 ---- Second line starts at 3 and ends at 6<br>
1 -------- They overlap so return true. The test case cover case with decimal<br>
0 0 ------ First line starts at 0 and ends at 0<br>
0 0 ------ Second line starts at 0 and ends at 0<br>
1 -------- The overlap so return true. The test case cover case with point comparison instead of line comparison<br>
-2 -1 ---- First line starts at -2 and ends at -1<br>
-1 0 ----- Second line starts at -1 and ends at 0<br> 
1 -------- They overlap so return true. The test case cover the overlap at the edge only<br>
-3 3 ----- First line starts at -3 and ends at 3<br>
0 0 ------ Second line starts at 0 and ends at 0 (a point)<br>
1 -------- They overlap so return true. The test case cover the line and point comparison<br>
-2 -1 ---- First line starts at -2 and ends at -1<br>
2 1 ------ Second line starts at 1 and ends at 2<br>
0 -------- They don't overlap so return false. The test case cover the comparison in negative field and positive field.<br>

Question B
---
The function implemented for this question is in QuestionB.py. The greaterthan function takes in two string a and b and return the string "equal" if a equal b, "greater" if a is greater than b, "less" if a is less than b, or "Please enter an string that start with number or -/+ sign and only include number after first character for the second/first input" if either a or b is in the wrong form (not number). In addition, the function also handle positive and negative number by allowing user to input in the form of +number, -number, or number<br>

The test for this function is implemented in Ching_Chuan_Wu_test.py. The script reads in test case from QuestionB.txt. QuestionB.txt is in the format of the following:<br>
number_of_testcase<br>
first_number-----space-----second_number<br>
result(greater or less or equal or wrongformat message)<br>
Repeat of the above two linea<br>

The following is the test case in QuestionB.txt and their explanations:<br>
9 ------------------ There are nine test cases<br>
1.2 1.1 ------------ a=1.2 and b=1.1<br>
greater ------------ a is greater than b<br>
0.3 0.4 ------------ a=0.3 and b=0.4<br>
less --------------- a is less than b. It covers case with decimal<br>
asd fee ------------ a=asd and b=fee<br>
Please enter... ---- wrong-format message because asd and fee is not numbers<br>
-2 3 --------------- a=-2 and b=3<br>
less --------------- a is less than b. It covers case with negative number and positive number comparison<br>
+2 +2 -------------- a=2 and b=2<br>
equal -------------- a is equal to b. It covers case of equal and use of + sign<br>
-2 -1 -------------- a=-2 and b=-1<br>
less --------------- a is less than b. It covers case with positive number to negative number comparison<br>
-22 +asdf ---------- a=-22 and b=asdf<br>
Please enter...----- wrong-format message because asdf is not an number<br>
-asd 4 ------------- a=-asd and b=4<br>
Please enter...----- wrong-format message because asd is not an number<br>
+inf -inf ---------- a=inf and b=-inf<br>
greater ------------ a is greater than b. It covers edge case of infinity which is the maximum that a float can be<br>

Question C
---
The library is implemented in QuestionC.py. The idea is based on my understanding that cache is used to retrieve data from memory rather than disk for faster retrieval. Thus, my library will define the cache on memory stack that can be retrieved before the function goes to disk to get the data. The usage are as following:<br>
1. import the library
    ```
    import QuestionC
    ```
2. Create cache server
    ```
    server_cache = QuestionC.server_cache()
    ```
    By default, server_cache class will be initialized with (max_size=5, othersevers=None,server_port=83, limit=10, expire=5) where max_size is the maximum number of cache that the server hold, otherservers are list of other servers currently running online (in form of tuple: (ip,port)), server_port is the port that the cache server listen for incoming request, limit is the time limit on every socket operation in second, and expire is time that each cash live in the system in minutes. By default, the cache server can be initialize with no input for the first server. However, the field otherservers need to be provided for additional server so that it communicate with previously established server. The overall workflow for the initialization are the following:<br>
    1. ALl fields in the class are initialized with the input or default value
    2. A child thread is created to listen on incoming request from other server using the same cache library
    3. If otherservers field is provided, it then notify all servers currently online using the provided ip address and port number so that all other server register this newly created server.
    4. It also get cache from other server so that the cache are consistence across all server. As a result, if we have server1 running already with cache for get_string function stored and we create server2 with ip address and port number of the cache server running on server1, then the cache server running on server2 will have the same cache store in memory as server1 even server2 have not yet received any request.<br>
3. Allow the server to use the cache server in the function that it provides. In the following, we assume that the library is used with a server that allows client to call get_string function provided by the server.
    ```
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
    ```
    Here, get_string is a function that run on the server which listen for client to call get_string function. When the function is called, it first search in the cache using server_cache.find_cache (sever_cache is initialized in step 2, usually when the server came online and start running). If what the function return is in the cache already, the function just return what it got in the cache. otherwise, it go ahead and retrieve data. After it did the expensive data retrieval, it then add the data to the cache using server_cache.add_cache so that next time when the same function is called, the data can be acquired from cache. In addition, the same cached is sent to other servers currently running for data consistency across servers.<br>
4. Finally, we stop the cache when we want to stop the server<br>
    ```
    server_cache.stop_listen()
    ```
The following are the explanation of how each criteria is handled:<br>

<h4>Simplicity. Integration needs to be dead simple</h4>
The library can be easy used in the server-side code by importing the module. Then calling add cache function in each function that need to retrieve expensive data so that the data stay in the memory stack.<br>

<h4>Resilient to network failures or crashes</h4>
The server_cache class can communicate with other server_cache classes running with other servers using python socket module with try and except block. Thus, the network failures of other server will not raise exception and stop the current server_cache class. On the other hand, the crash of the current server will not effect other server and the same library running there too. Since the cache is saved in memory stack, the crash of the server will wipe out all the cache and the restart of the server will restart the server_cache class with empty cache. One possible solution of keeping all the cache even the server crash or stop is saving all the cache in remote database and have the server_cache class load those data when initializing. However, this is out of scope for this question but it can be useful in real-life cases.<br> 

<h4>Near real time replication of data across Geolocation. Writes need to be in real time</h4>
Each call to add cache in a server will also call add cache in other server through socket module. Thus, the cache in all server are updated at around the same time.

<h4>Data consistency across regions</h4>
With real-time replication of data across multiple cache server and each cache server running on different servers in different location/region, data consistency is achieved. 

<h4>Locality of reference, data should almost always be available from the closest region</h4>
With the data to be consistent across all servers in near real-time, the requested data are available in all servers even the request is only made in one server.<br>

<h4>Flexible Schema</h4>
In the server_cache class, the cache is saved as multiple node classes forming a linked list which act as queue. The data is stored in the node as object and thus can be any type. Each node is paired with the dictionary to achieve constant access even for the node in the middle of the queue. There are two dictionary include mapping from function_name (string) to object id and object id to the node. Thus, The Schema is flexible and any datatype can be paired with the function name and object id.

<h4>Cache can expire</h4>
In the lookup method, the timestemp is checked before the cache is returned. If the different of the current time to the timestamp is larger than or equal to the expired time that is set during the initialization, the node containing the cache and the corresponding entry in the dictionary will be deleted.<br>

<br>
<br>
Similar with question A and B, question C is also tested in Ching_Chuan_Wu_test.py. However, the test cases are not asserted because the variation (order and timing) of setting up each server and integrate the dictionary will bring different result. In Ching_Chuan_Wu_test.py, the following happened for question C:<br>
1. It call the script server1.py which act as a server running online and listening for input. <br>
2. The server first initiate the server_cache<br>
3. It than reads Server1.txt as user input where each input serve as request from client.<br>
4. It then received get_string call (The cache is then updated)<br>
5. It then setup another server by running server2.py. server2.py also act as another server running online and provide the same get_string function for client to call<br>
6. The initialization of the server_cache on server2 is called by server_cache = QuestionC.server_cache(5, [('10.0.0.134', 83)], 84, 10) where 10.0.0.134 is the ip of the first sever cache and 83 is the port that the first server cache binds on.<br>
7. The server2 then received get_string request (also read from Server2.txt as input).<br>
8. Then the data is get from cache because the same function have been called on server1<br>
9. server2 then shut down itself.<br>
10. server1 then received get_string request again and return the data from the cache.<br>
11. server1  then shut down itself.<br>
    
<br>
To test question C manually, simply delete Server1.txt. Than running server1.py (python server1.py) will prompt for listening for input. Note that after the first call of get_string, server2 will start too. Deleting the Server2.txt will also allows you to input the request and control the flow. Note that the valid input for server1 and server2 are get_string, wait, and exit<br>
<br>
In addition, I have to mentioned that the [('10.0.0.134', 83)] used to initialize server cache on server2 will attempt to connect to the provided ip address and port. However, those are the ip of my machine and port that I used to initialized server cache on server1. Note that the server_cache will prompt you with the ip address and port it is running on when initialized. Please change the ip and port accordingly when initialized 2nd or more serve_cache.<br>

Ching_Chuan_Wu_test.py
---
Running this script (python Ching_Chuan_Wu_test.py) will simply run through the test case for all question. It will then print the result out in the terminal. You can follow on what happened by simply read through the log that have been printed out. For question A and B, the test case can be changed by changing QuestionA.txt and QuestionB.txt (Please read the section Question A and Question B above for what format the text file should be). The test for Question C cannot be changed but the manual testing can be done by running server1.py and server2.py manually without Server1.txt and Server2.txt. 

Disclaimer
---
I take pride in all code that I wrote. Especially for Question C, I only used standard library such as socket, pickle, threading, time, and datetime. All the logic for storing cache in memory stack, having cache to expire, the whole infrastructure is original. Even the queue that is implemented by linked list which is implemented by node which is the class that I created is implemented without using any 3rd party library. This is truely a build from nothing project. In other words, I only needed a computer with internet connection to build all these. Consider I never used socket module in python (I got some experince writing server and client code in C++ using RPC library) and multi-threading in python (also have some experience in C for multi-threading), I am proud of what I have created especially it only took me 4 days. You are free to use the code for personal project but please let me know if you do so. However, you are not allow to distribute the code without my acknowledge. The project might also be further updated in future for better functionality and efficiency. Please don't hesitate to contact me if you have any recommendation of what to change!<br>

You can find my through email: 0429charlie@gmail.com

© Copyright 2020, Ching Chuan Wu, All Rights Reserved
