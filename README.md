# Pressure Control Project using Django, Python, and MQTT

This is a software project aimed at communicating with an MQTT broker for receiving payloads and manipulating a ladder supervisory system in an ICAD (Industrial Control and Data Acquisition) environment. The primary objective is to implement a PID (Proportional-Integral-Derivative) control algorithm to regulate pressure in an industrial setting. The project leverages Django and Python technologies to create a web application for configuring and monitoring the pressure control system.

## Technologies Used

- **Django**: A Python-based web framework that facilitates the rapid and clean development of complex web applications.
- **Python**: A versatile and powerful programming language widely used for application development.
- **MQTT**: A lightweight and efficient messaging protocol for communication between devices in sensor networks.
- **Ladder Supervisory System**: A monitoring and control system that visualizes the status of devices in an industrial environment.
- **PID Control**: A control algorithm that uses proportional, integral, and derivative terms to regulate processes in dynamic systems.
## Preview

<div align=center>
<img src="https://i.imgur.com/bwPTSap.png">
</div>

## Setup and Execution

Follow the steps below to set up and run the project in your environment:

1. **Clone the repository:**

      ```bash
      git clone https://github.com/andersonlimacrv/MQTT-ICAD-ASYNC.git
      cd MQTT-ICAD-ASYNC
      ```

2. **Create a virtual environment:**

      ```bash
      python -m venv venv
      source venv/bin/activate   # On Windows: venv\Scripts\activate
      ```

3. **Install dependencies:**

      ```bash
      pip install -r requirements.txt
      ```

4. **Configure environment variables:**
   Rename the `.env.example` file to `.env` and configure the necessary variables, such as MQTT broker settings.

5. **Run database migrations:**

      ```bash
      python manage.py migrate
      ```

6. **Start the Django server:**

      ```bash
      python manage.py runserver
      ```

7. **Access the application:**
   Open a web browser and visit `http://localhost:8000` to access the project's web interface.

---
