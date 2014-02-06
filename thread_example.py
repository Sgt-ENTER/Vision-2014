# Example for controlling different threads
import threading
import time

goal_event = threading.Event()
catch_event = threading.Event()

def find_goal():
    while True:
        goal_event.wait() # Block until goal event is set
        print "Finding goal"

def catch_ball():
    while True:
        catch_event.wait() # Block until catch event is set
        print "Catching ball"

if __name__ == "__main__":
    # Create and start goal thread
    goal_thread = threading.Thread(target=find_goal, name="findgoal")
    goal_thread.daemon = True
    goal_thread.set() # Allow goal thread to run initially
    goal_thread.start()
    
    # Create and start catch thread
    catch_thread = threading.Thread(target=catch_ball, name="catchball")
    catch_thread.daemon = True
    catch_event.clear() # Do not allow catch thread to run initially
    catch_thread.start()
    
    while True:
        # Infinite loop to keep the main thread running
        # and waiting for connections
        # Makes breaking out of program with Ctrl-C easier
        time.sleep(1)
        if goal_event.is_set():
            goal_event.clear()
            catch_event.set()
        else:
            catch_event.clear()
            goal_event.set()
