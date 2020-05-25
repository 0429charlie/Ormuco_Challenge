import socket, pickle
import threading
import time

from datetime import datetime
from threading import Thread


# Node for linked list working as queue here
# It has attribute linking it to the previous and the next node
# It also know if it is the head or tail of the linked list
# The content is what people save in cache. Type can varies depend on what program this library is running with
class Node:
    def __init__(self):
        self.next = None
        self.pre = None
        self.head = True
        self.tail = False
        self.content = None
        self.key = None
        self.fn_name = None
        self.timestemp = None


# The queue is consisted of nodes in the form of linked list
# The map uses id(node) as key and node itself as value
# The dic uses function name (provided by user) as key and id(node) as value
# The class also initialized socket binded on given port (83 by default) which can later be used to listen for incoming request
class server_cache:
    # Initialization. It create new thread that listening for incoming request, Initialize all fields, and send notification to other server to register itself.
    def __init__(self, max_size=5, othersevers=None,server_port=83, limit=10, expire=5):
        self.listening = True
        self.head = None
        self.tail = None
        self.max_size = max_size
        self.expire = expire
        # from object id to node holding that object
        self.mapping = {}
        self.allservers = othersevers
        # dictionary to hold mapping from function name to object id (including those from previously established server)
        self.dic = {}
        # Get the server ip
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        # socket for server
        self.s = socket.socket()
        # Record the ip and port
        self.ip = ip
        self.server_port = server_port
        # Lock used to ensure atomoicity of queue update
        self.queue_lock = threading.Lock()
        # Start listening
        self.listening_thread = Thread(target=self.start_listen, args=(limit,))
        self.listening_thread.setDaemon(True)
        self.listening_thread.start()
        # Let sleep for 5 second so that new thread can run first and start listening before the main thread proceed
        time.sleep(5)
        # Then notify all servers online
        if self.allservers:
            self.allservers = set(self.allservers)
            count = len(self.allservers)
            for host in self.allservers:
                count = count-1
                h, p = host
                ss = socket.socket()
                ss.connect((h, p))
                if count==0:
                    ss.send(pickle.dumps(("init_last",(ip, server_port))))
                else:
                    ss.send(pickle.dumps(("init",(ip, server_port))))
                ss.shutdown(socket.SHUT_WR)
                ss.close()
        else:
            self.allservers = set()
        # Wait for a while so that self.dic is updated
        time.sleep(5)

    # Function to update the available servers
    # It record the new ip and port that the new server binds on. Intended only for private use for this class
    # String Int -> Void
    def add_server(self,newip, newport):
        self.queue_lock.acquire()
        try:
            self.allservers.add((newip,int(newport)))
        finally:
            self.queue_lock.release()

    # Function to delete the available servers
    # It delete the ip and port of the indicated server. Intended only for private use for this class
    # String Int -> Void
    def del_server(self,ip,port):
        self.queue_lock.acquire()
        try:
            self.allservers.remove((ip,int(port)))
        finally:
            self.queue_lock.release()

    # Function to add the object to the cache. The object can be in the cache already or not
    # It must be called every time the function that use this cache server in the user written program is called
    # Object String Bool -> Void
    def add_cache(self, inobject, fn_name, init=False):
        self.queue_lock.acquire()
        try:
            objectid = id(inobject)
            # Hit
            if objectid in self.mapping:
                # Get the node in the queue
                n = self.mapping[objectid]
                # If the node is not the head
                if not n.head:
                    # If, however, it is the tail
                    if n.tail:
                        # Update the new tail
                        n.pre.next = None
                        n.pre.tail = True
                        self.tail = n.pre
                    # If it is in the middle
                    else:
                        # Remove the node from the linked list
                        n.pre.next = n.next
                        n.next.pre = n.pre
                    # Update the current node to be the head
                    n.tail = False
                    n.pre = None
                    n.head = True
                    n.next = self.head
                    # Update the old head
                    self.head.pre = n
                    self.head.head = False
                    # Update the head in the cache class
                    self.head = n
            # Miss
            else:
                # If the cache is full
                if (len(self.mapping)>=self.max_size) and (self.max_size>0):
                    # Delete the tail and its entry in mapping
                    del self.mapping[self.tail.key]
                    new_tail = self.tail.pre
                    self.tail.tail = False
                    self.tail.head = False
                    self.tail.pre = None
                    self.tail.next = None
                    new_tail.tail = True
                    new_tail.next = None
                    self.tail = new_tail
                # Now, cache is guarantee to not be full. Let just add our new cache
                n = Node()
                n.content = inobject
                n.key = objectid
                n.fn_name = fn_name
                n.timestemp = datetime.now()
                # But first, let see if we have anything in the cache first
                # If we have empty cache
                if len(self.mapping)==0:
                    # Set node to also be the tail
                    n.tail = True
                    self.tail = n
                    self.head = n
                else:
                    # Otherwise, simply add the node as head
                    n.next = self.head
                    self.head.pre = n
                    self.head = n
                self.mapping[n.key] = n
                self.dic[fn_name] = n.key
            # update all server if not initializing or request from other servers so data are consistence
            if not init:
                for host in self.allservers:
                    h, p = host
                    ss = socket.socket()
                    ss.connect((h, p))
                    ss.send(pickle.dumps(("data",(inobject,fn_name,True))))
                    ss.shutdown(socket.SHUT_WR)
                    ss.close()
        finally:
            self.queue_lock.release()

    # Function to delete the expired node
    def del_node(self,objectid):
        n = self.mapping[objectid]
        if n.head and n.tail:
            # Actually, we don't need to do anything here
            # Simply del this node from self.mapping will works
            pass
        if n.head:
            self.head = n.next
            self.head.pre = None
            n.next = None
            n.head = False
        if n.tail:
            self.tail = n.pre
            self.tail.next = None
            n.pre = None
            n.tail = False
        else:
            n.pre.next = n.next
            n.next.pre = n.pre
            n.pre = None
            n.next = None
        # Also delete from self.mapping
        del self.mapping[objectid]

    # Function to find the requested object given the object id
    # Note that object id can be acquired from self.dic[key] where key is the function name
    # It must be called before every time the function that use this cache server in the user written program execute it expensive calculation
    # INT -> Object or None
    def find_cache(self,objectid):
        # Hit
        if objectid in self.mapping:
            # Check timestemp
            n = self.mapping[objectid]
            time_difference = datetime.now() - n.timestemp
            in_second = time_difference.total_seconds()
            in_minute = in_second / 60
            # Delete the node if expired
            if in_minute >= self.expire:
                self.del_node(objectid)
                return None
            else:
                return self.mapping[objectid].content
        # Miss
        else:
            return None

    # Thread to handle incoming request
    # Intended only for private use for this class
    def handle_request(self,c):
        # Receive data and close the connection
        data = c.recv(4096)
        c.shutdown(socket.SHUT_WR)
        c.close()
        # See what request it is (all request are from other servers)
        pickle_data = pickle.loads(data)
        fn, body = pickle_data
        # New server created and server library need to be updated
        if fn == "init":
            ip, port = body
            self.add_server(ip, port)
        # New function registered in other servers or this server is newly created and cache need to be consistence with other servers
        elif fn == "data":
            obj, fn_name, init = body
            self.add_cache(obj,fn_name,init)
        # One of the servers destroyed and this server need to delete the destroyed server
        elif fn == "del":
            ip, port = body
            self.del_server(ip, port)
        # New server created and server library need to be updated. Also, cache of the new server need to be consistence with this server
        elif fn == "init_last":
            ip, port = body
            self.add_server(ip, port)
            # In addition, we send the queue back so that the newly created server have the same queue
            # It need to be done consecutively (no update before the queue is sent)
            self.queue_lock.acquire()
            current_node = self.head
            while current_node!=None:
                ss = socket.socket()
                ss.connect((ip, port))
                ss.send(pickle.dumps(("data", (current_node.content,current_node.fn_name, True))))
                ss.shutdown(socket.SHUT_WR)
                ss.close()
                current_node = current_node.next
            self.queue_lock.release()

    # Function to start listening the incoming request on new thread
    # Int -> Void
    def start_listen(self, limit):
        # Bind the socket to the port provided (port 83 if not provided)
        self.s.bind((self.ip, self.server_port))
        # Time out for listening
        self.s.settimeout(5)
        self.s.listen(limit)
        print("start listening on " + self.ip + " port " + str(self.server_port))
        while True:
            if self.listening:
                try:
                    # Get the request and create new thread to handle each request
                    c, address = self.s.accept()
                    t = Thread(target=self.handle_request, args=(c,))
                    t.setDaemon(True)
                    t.start()
                    # Join the thread so that request is completed in order
                    t.join()
                except socket.timeout:
                    pass
            else:
                break
        self.s.close()

    # Function to call when we want to close the cache server
    def stop_listen(self):
        # Allow the thread listening the incoming request to stop
        self.listening = False
        # update all server to delete this server
        for host in self.allservers:
            h, p = host
            ss = socket.socket()
            ss.connect((h, p))
            ss.send(pickle.dumps(("del", (self.ip, self.server_port))))
            ss.shutdown(socket.SHUT_WR)
            ss.close()
        # Wait for the thread listening for the request to stop
        self.listening_thread.join()
        print("chache server closed. Please create a new one to start using the cache server again.")
