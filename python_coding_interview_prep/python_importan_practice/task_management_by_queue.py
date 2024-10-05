import queue
import threading
import time

# Task structure with priority, task_id, and task_time (execution time)
class Task:
    def __init__(self, priority, task_id, task_time):
        self.priority = priority  # Task priority
        self.task_id = task_id    # Task ID
        self.task_time = task_time  # Time the task takes to complete (in seconds)

    # This method allows comparison based on task priority
    def __lt__(self, other):
        return self.priority < other.priority

# Function to process tasks
def process_task(task):
    print(f"Processing task {task.task_id} with priority {task.priority} and execution time: {task.task_time} seconds")
    time.sleep(task.task_time)  # Simulate task execution time
    print(f"Task {task.task_id} completed")

# Task manager function
def task_manager(task_queue):
    while not task_queue.empty():
        task = task_queue.get()
        try:
            process_task(task)
        finally:
            task_queue.task_done()

# Create a priority queue
task_queue = queue.PriorityQueue()

# Dictionary to keep track of tasks for updates and removal
task_dict = {}

# Function to add a task
def add_task(priority, task_id, task_time):
    if task_id not in task_dict:
        task = Task(priority=priority, task_id=task_id, task_time=task_time)
        task_queue.put(task)
        task_dict[task_id] = task
        print(f"Task {task_id} added with execution time {task_time} seconds.")
    else:
        print(f"Task {task_id} already exists.")

# Function to update a task's priority or time
def update_task(task_id, new_priority=None, new_time=None):
    if task_id in task_dict:
        task = task_dict[task_id]
        if new_priority is not None:
            task.priority = new_priority
        if new_time is not None:
            task.task_time = new_time
        # Re-queue the updated task with new priority or time
        task_queue.put(task)
        print(f"Task {task_id} updated: priority={new_priority}, time={new_time} seconds.")
    else:
        print(f"Task {task_id} not found.")

# Function to remove a task
def remove_task(task_id):
    if task_id in task_dict:
        del task_dict[task_id]
        print(f"Task {task_id} removed.")
    else:
        print(f"Task {task_id} not found.")

# Add initial tasks with priority and execution time
add_task(2, 1, 2)  # Task 1 with 2 seconds of execution time
add_task(1, 2, 4)  # Task 2 with 4 seconds of execution time
add_task(3, 3, 1)  # Task 3 with 1 second of execution time

# Update task 2 before processing
update_task(2, new_priority=0, new_time=3)  # Update task 2 with new priority and execution time

# Remove task 3 before processing
remove_task(3)

# Start task manager threads
num_threads = 2
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=task_manager, args=(task_queue,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete processing
for thread in threads:
    thread.join()

print("All tasks have been processed.")
