# DES-Reducer

DES-Reducer is a Python application designed to monitor and reduce Digital Eye Strain (DES) by analysing user behaviour through webcam input. The programme tracks various parameters such as eye movements, blinking frequency, screen brightness, and posture to provide real-time feedback and suggestions for reducing eye strain.

## Features

- **Face Detection**: Identifies the user's face to monitor eye-related metrics.  
- **Blink Detection**: Monitors blinking frequency to ensure eyes are adequately lubricated.  
- **Screen Brightness Adjustment**: Assesses ambient light and screen brightness, providing recommendations for optimal settings.  
- **Posture Monitoring**: Evaluates user posture to prevent strain related to improper seating positions.  
- **Yawning Detection**: Detects yawning as an indicator of fatigue, suggesting breaks when necessary.  
- **Graphical User Interface (GUI)**: Provides an intuitive interface for users to interact with the application.  
- **Notifications**: Sends alerts and suggestions based on the analysis to help reduce eye strain.  

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Tom0267/DES-Reducer.git
   cd DES-Reducer
   ```

2. **Install Dependencies**:  
   Ensure you have Python installed. It is recommended to use a virtual environment.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python Main.py
   ```

## Usage

After running the application, the GUI will launch and access your webcam. Please make sure your webcam is functional and properly positioned. The application will provide real-time feedback and notifications to help you adjust your environment and habits to reduce digital eye strain.

![image](https://github.com/user-attachments/assets/b7987f3d-11d4-4155-ae83-a80a68f3f65b)

## Modules Overview

- **Main.py**: The main entry point of the application.
- **Config.py**: Contains configuration settings for the application.  
- **DistanceCalc.py**: Calculates the distance between the user and the screen.  
- **EyeArea.py**: Analyses the area of the eyes to monitor blinking and potential redness.  
- **EyeMovements.py**: Tracks and analyses eye movement patterns.  
- **EyeRedness.py**: Detects redness in the eyes as an indicator of strain.  
- **FaceDetector.py**: Handles face detection functionalities.  
- **FaceTrack.py**: Tracks facial movements to assess posture and alignment.  
- **GUI.py**: Manages the graphical user interface components.    
- **Posture.py**: Monitors user posture to provide feedback on seating positions.  
- **ScreenBrightness.py**: Assesses and provides recommendations on screen brightness.  
- **Yawn.py**: Detects yawning to suggest breaks when fatigue is detected.  
- **graph.py**: Generates graphical representations of survey results.  
- **notifier.py**: Manages notifications and alerts to the user.  

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes. Ensure that your code adheres to the project's coding standards and includes appropriate documentation.

## Acknowledgements

Special thanks to the open-source community for providing the tools and libraries that made this project possible.

---

*Note: This application requires access to your system's webcam and may process personal data. Ensure you are comfortable with this and understand the privacy implications before use.*
