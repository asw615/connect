# Connected: Enhancing Student Well-Being with Sociograms

**Authors**:  
- Søren Søndergaard Meiner (SM)
- Laura Sørine Voldgaard (LV)

**Institution**:  
School of Communication and Culture, Aarhus University  

---

## Overview

Connected is a web-based platform designed to enhance student well-being by visualizing social dynamics in classrooms through **sociograms**. The tool aims to empower teachers to better understand and manage student relationships, fostering a supportive and inclusive learning environment.

The project focuses on students in grades 7–9, where the decline in well-being is particularly pronounced. Connected addresses this by providing insights into both social and academic well-being, bridging the gap left by traditional quantitative surveys.

---

## Features

- **Interactive Sociograms**: Visual representation of classroom social networks using gradient scales for nodes and color-coded edges to reflect relationships.
- **Data Collection**: Customizable questionnaires that collect insights on student well-being, motivation, and academic relationships.
- **Teacher-Friendly Dashboard**: Easy-to-use interface for teachers to view and interpret sociograms and insights.
- **Ethical and Practical Guidelines**: Built-in resources to ensure responsible use of data.

---

## Project Goals

1. **Immediate Impact**: Provide actionable insights for teachers to address classroom dynamics.
2. **Scalable Design**: Develop a modular platform that can be expanded with features like group formation and AI-based analytics.
3. **User-Focused**: Balance rich data collection with user-friendly visualizations and practical application.

---

## Technical Specifications

### Frontend
- **Frameworks**: 
  - HTML and CSS for structure and styling.
  - Bootstrap 4 for responsive design.
  - JavaScript and jQuery for interactivity.
- **Visual Elements**: 
  - Carousel sliders and navigation bars.
  - Color-coded sociograms for dynamic representation.

### Backend
- **Framework**: Flask to integrate Python functionalities with the website.
- **Data Processing**:
  - Questionnaires designed to collect student input.
  - Sociograms generated using the Python library `igraph`.
- **Security**:
  - Login functionality to restrict access.
  - Plans for implementing encrypted data storage and secure connections.

---

## Product Development

### Timeline
1. **Minimum Viable Product (MVP)**: A functional sociogram generator with data collection capabilities.
2. **Mid-Tier Product**: A fully integrated web application for teachers to manage and access data seamlessly.
3. **Ideal Product**: Advanced tools like AI-driven group formation, sentiment analysis, and personalized recommendations.

### Sociogram Design
- **Nodes**: Represent students, with colors reflecting self-perceived well-being.
- **Edges**: Show positive and negative relationships based on survey responses.
- **Layout**: Uses the Fruchterman-Reingold algorithm for intuitive visualization.

---

## How to run the website
1. Open your IDE (Visual studio code, psychopy e.g.) and open the folder with the website. 
2. Type "source /path_to_your_folder/connected/bin/activate". Remember to change "path_to_your_folder" to where your folder is located
3. Type "flask run" in your terminal
4. Open up your browser and go to "http://127.0.0.1:5000/index". The link will maybe differ, but you can see the link in your terminal starting with "http://". Remember to end the link with "/index"
5. To stop the server again hit "CTRL" and "C" at the same time.

---

## Challenges and Ethical Considerations

- **Conceptual Challenges**:
  - Differentiating Connected from existing tools like Klassetrivsel.
  - Maintaining simplicity while adding advanced features.
- **Ethical Concerns**:
  - Ensuring privacy and compliance with GDPR.
  - Avoiding negative impacts, such as fostering harmful comparisons or priming negative thoughts.
- **Data Security**:
  - Plans to implement Transport Layer Security (TLS) and use secure login systems like UNI-login.

---

## Future Directions

1. **Independent Development**: Expand Connected with features like:
   - AI-driven sentiment analysis of free-text responses.
   - Group formation tools using machine learning.
   - Enhanced visualization techniques for large classrooms.
2. **Collaboration with Klassetrivsel**: Partner with an established platform to integrate advanced features, leveraging their existing infrastructure and user base.


 
