# CPU Scheduling Simulator 🖥️

An interactive Python-based simulator for classic **Operating Systems CPU Scheduling Algorithms**, featuring textual performance metrics and graphical Gantt chart visualization using `matplotlib`.

---

## 🚀 Features
- **Supported Algorithms:**
  1. **FCFS** (First-Come, First-Served)
  2. **SJF** (Shortest Job First - Non-Preemptive)
  3. **HRRN** (Highest Response Ratio Next)
  4. **Round Robin (RR)** (with customizable time quantum)
  5. **SRTF** (Shortest Remaining Time First - Preemptive)
  6. **MLFQ** (Multilevel Feedback Queue with 4 configurable queues)
- **Context Switching:** Configurable context switch overhead added between transitions.
- **Visualizations:** Generates an intuitive Gantt chart displaying execution intervals and arrival markers ($(\times)$).
- **Performance Metrics:** Computes per-process and average metrics (Waiting Time, Turnaround Time, Response Time).

---

## 📋 Requirements
- Python 3.8+
- `matplotlib`

You can install the required package via pip:
```bash
pip install matplotlib
