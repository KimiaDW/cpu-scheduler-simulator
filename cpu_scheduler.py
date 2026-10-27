import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.response_time = -1        
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.queue_level = 0  
        self.started = False     


def print_table(processes):
    wt = tat = rs = 0
    print("\nProcess\tAT\tBT\tRS\tWT\tTAT")

    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.response_time}\t{p.waiting_time}\t{p.turnaround_time}")
        wt += p.waiting_time
        tat += p.turnaround_time
        rs += p.response_time
    
    print(f"avg_waiting_time = { wt/len(processes) }\navg_turnaround_time = { tat/len(processes) }\nave_response_time = { rs/len(processes) }")


def fcfs(processes, context_switch):
    time = 0
    gantt_chart = []
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)

    for process in sorted_processes:

        if time < process.arrival_time:
            time = process.arrival_time

        start_time = time
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = start_time - process.arrival_time
        
        gantt_chart.append((process.pid, start_time, time))
        time += context_switch

    print_table(processes)

    return gantt_chart


def sjf(processes, context_switch):
    time = 0
    gantt_chart = []
    queue = []
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_index = 0

    for process in sorted_processes:

        if time < process.arrival_time:
            time = process.arrival_time

        while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
            queue.append(sorted_processes[ready_index])
            ready_index += 1

        queue.sort(key=lambda p: p.burst_time)
        process = queue.pop(0)

        start_time = time
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = start_time - process.arrival_time


        gantt_chart.append((process.pid, start_time, time))
        time += context_switch

    print_table(processes)

    return gantt_chart


def hrrn(processes, context_switch):
    time = 0
    queue = []
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_index = 0
    gantt_chart = []

    for p in sorted_processes:

        if p.arrival_time > time:
            time = p.arrival_time

        while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
            queue.append(sorted_processes[ready_index])
            ready_index += 1
            
        for p in queue:
            p.waiting_time = time - p.arrival_time
            p.response_ratio = p.waiting_time / p.burst_time

        process = max(queue, key=lambda p: p.response_ratio)
        queue.remove(process)

        start_time = time
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = start_time - process.arrival_time

        gantt_chart.append((process.pid, start_time, time))
        time += context_switch

    print_table(processes)

    return gantt_chart


def round_robin(processes, quantum, context_switch):
    time = 0
    queue = []
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_index = 0
    gantt_chart = []

    if sorted_processes[0].arrival_time > time:
        time = sorted_processes[0].arrival_time

    while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
        queue.append(sorted_processes[ready_index])
        ready_index += 1

    while queue:
        process = queue.pop(0)
        start_time = time
        if process.response_time == -1:
            process.response_time = start_time - process.arrival_time 

        if process.remaining_time > quantum:
            time += quantum
            process.remaining_time -= quantum
        else:
            time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            
        gantt_chart.append((process.pid, start_time, time))
        time += context_switch

        while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
            queue.append(sorted_processes[ready_index])
            ready_index += 1

        if process.remaining_time > 0:
            queue.append(process)

        if not queue and ready_index < len(sorted_processes):
            time = sorted_processes[ready_index].arrival_time

            while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
                queue.append(sorted_processes[ready_index])
                ready_index += 1

    print_table(processes)

    return gantt_chart


def srtf(processes, quantum, context_switch):
    time = 0
    gantt_chart = []
    queue = []
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_index = 0

    if sorted_processes[0].arrival_time > time:
        time = sorted_processes[0].arrival_time

    while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
        queue.append(sorted_processes[ready_index])
        ready_index += 1

    while queue:

        queue.sort(key=lambda p: p.remaining_time)
        process = queue.pop(0)

        start_time = time
        if process.response_time == -1:
            process.response_time = start_time - process.arrival_time

        quantum_left = quantum            

        while quantum_left and process.remaining_time:

            if ready_index < len(sorted_processes):
                next_arrival = sorted_processes[ready_index].arrival_time
            else:
                next_arrival = None

            if next_arrival is None:
                execution_time = min(quantum_left, process.remaining_time)
            else:
                execution_time = min(quantum_left, process.remaining_time, next_arrival - time)

            time +=  execution_time
            process.remaining_time -=  execution_time
            quantum_left -=  execution_time

            if time == next_arrival:
                while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
                    queue.append(sorted_processes[ready_index])
                    ready_index += 1

                if min(p.remaining_time for p in queue) < process.remaining_time:
                    break

        if process.remaining_time:
            queue.append(process)
        else:
            process.remaining_time = 0
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, start_time, time))
        time += context_switch            

        if not queue and ready_index < len(sorted_processes):
            time = sorted_processes[ready_index].arrival_time           

        while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
            queue.append(sorted_processes[ready_index])
            ready_index += 1

    print_table(processes)

    return gantt_chart


def execute_process(p, algorithm, quantum, time, next_arrival, next_p_burst=None):
    start_time = time
    
    if not p.started:
        p.response_time = start_time - p.arrival_time
        p.started = True
        
    if algorithm in ["FCFS", "SJF", "HRRN"]:
        exec_time = p.remaining_time
        time += exec_time
        p.remaining_time = 0

    elif algorithm == "RR":
        exec_time = min(quantum, p.remaining_time)
        time += exec_time
        p.remaining_time -= exec_time

    if algorithm == "SRTF":
        limit = min(quantum, p.remaining_time) 
               
        if next_arrival is not None:
            time_to_arrival = next_arrival - time
            
            if 0 < time_to_arrival < limit:
                remaining_at_arrival = p.remaining_time - time_to_arrival
                
                if next_p_burst is not None and next_p_burst < remaining_at_arrival:
                    exec_time = time_to_arrival
                else:
                    exec_time = limit
            else:
                exec_time = limit
        else:
            exec_time = limit

        time += exec_time
        p.remaining_time -= exec_time

    return start_time, time


def mlfq(processes, queue_algorithms, quantums, context_switch):
    time = 0
    ready_index = 0
    queues = [[] for _ in range(4)]
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    gantt_chart = []

    while ready_index < len(sorted_processes) or any(queues):
        while ready_index < len(sorted_processes) and sorted_processes[ready_index].arrival_time <= time:
            queues[0].append(sorted_processes[ready_index])
            ready_index += 1

        if not any(queues):
            time = sorted_processes[ready_index].arrival_time
            continue

        for level in range(4):

            if queues[level]:

                if queue_algorithms[level] == "SRTF":
                    queues[level].sort(key=lambda p: p.remaining_time)
                    process = queues[level].pop(0)

                if queue_algorithms[level] == "SJF":
                    queues[level].sort(key=lambda p: p.burst_time)  
                    process = queues[level].pop(0)

                if queue_algorithms[level] == "HRRN":

                    for p in queues[level]:
                        p.waiting_time = time - p.arrival_time
                        p.response_ratio = p.waiting_time / p.burst_time

                    process = max(queues[level], key= lambda p: p.response_ratio)
                    queues[level].remove(process)

                if queue_algorithms[level] == "FCFS" or queue_algorithms[level] == "RR":
                    process = queues[level].pop(0)

                next_arrival = None
                next_burst = None

                if ready_index < len(sorted_processes):
                    next_arrival = sorted_processes[ready_index].arrival_time
                    next_burst = sorted_processes[ready_index].burst_time

                start, end = execute_process(process, queue_algorithms[level], quantums[level], time, next_arrival, next_burst)
                time = end
                gantt_chart.append((process.pid, start, time))

                if process.remaining_time > 0:
                    if (time - start) >= quantums[level]:
                        next_level = min(level + 1, 3)
                        queues[next_level].append(process)
                    else:
                        queues[level].append(process)
                else:
                    process.completion_time = time
                    process.turnaround_time = time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time

                time += context_switch
                break
            
    print_table(processes)
    return gantt_chart


def draw_gantt_chart(gantt_chart, processes):
    fig, ax = plt.subplots(figsize=(12, 4))
    pids = [p.pid for p in processes]
    process_order = {pid: i for i, pid in enumerate(sorted(pids))}

    plt.yticks(range(len(pids)), sorted(pids))

    for pid, start, end in gantt_chart:
        y = process_order[pid]
        ax.barh(y, width=end-start, height=0.5, left=start)

    for p in processes:
        ax.plot(p.arrival_time, process_order[p.pid], marker='x', color='red', markersize=8)

    ax.set_xlabel("Time")

    max_time = max(end for _, _, end in gantt_chart)

    ax.set_xticks(range(0, max_time + 2))

    ax.grid(axis='x', linestyle='--', alpha=0.5)
    plt.show()

# processes = [Process('p1', 0, 14), Process('p2', 2, 9), Process('p3', 5, 4), Process('p4', 6, 8)]
# processes = [Process('p1', 2, 4), Process('p2', 2, 2), Process('p3', 4, 5), Process('p4', 7, 6)]
processes = [Process('p1', 0, 4), Process('p2', 2, 7), Process('p3', 5, 6), Process('p4', 6, 3)]
# processes = [Process('p1', 0, 4), Process('p2', 2, 6), Process('p3', 2, 6), Process('p4', 10, 4)]


def select_algorithm():
    print("\nSelect CPU Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF")
    print("3. HRRN")
    print("4. Round Robin")
    print("5. SRTF")
    print("6. MLFQ")

    choice = int(input("Enter your choice (1-6): "))
    return choice

def select_queue_algorithms():
    allowed1 = ["RR", "SRTF"]
    allowed2 = ["FCFS", "SJF", "HRRN"]
    queue_algorithms = []
    quantums = []

    for i in range(3):
            while True:
                algorithm = input(f"Select algorithm for Queue {i} {allowed1}: ").upper()
                if algorithm in allowed1:
                    queue_algorithms.append(algorithm)
                    break
                else:
                    print("Invalid algorithm. Try again.")

            q = int(input(f"Enter Time Quantum for Queue {i}: "))
            quantums.append(q)
            
    while True:
        algorithm = input(f"Select algorithm for Queue {i} {allowed2}: ").upper()
        if algorithm in allowed2:
            queue_algorithms.append(algorithm)
            break
        else:
            print("Invalid algorithm. Try again.")    
    quantums.append(None)

    return queue_algorithms, quantums

choice = select_algorithm()
context_switch = int(input("Enter Context Switch Time: "))

if choice == 1:
    g = fcfs(processes, context_switch)

elif choice == 2:
    g = sjf(processes, context_switch)

elif choice == 3:
    g = hrrn(processes, context_switch)

elif choice == 4:
    quantum = int(input("Enter Time Quantum: "))
    g = round_robin(processes, quantum, context_switch)

elif choice == 5:
    quantum = int(input("Enter Time Quantum for SRTF: "))
    g = srtf(processes, quantum, context_switch)

elif choice == 6:
    queue_algorithms, quantums = select_queue_algorithms()
    g = mlfq(processes, queue_algorithms, quantums, context_switch)

else:
    print("Invalid choice!")
    exit()
    
draw_gantt_chart(g, processes)