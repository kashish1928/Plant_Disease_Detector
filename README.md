# Plant Whisperer
<div style="text-align: center;">
  <img src="src/images/template.png" style="width: 400px; height: 400px; margin: 0 auto;" />
</div>


## Overview
Crop diseases pose a significant threat to global food security, especially in regions lacking proper infrastructure for rapid disease identification. To address this challenge, we present a web application that leverages the widespread adoption of smartphones and cutting-edge transfer learning models. Our solution aims to streamline the process of crop disease diagnosis, providing users with insights into disease types, suitable treatments, and preventive measures.

## Key Features
- **Disease Detection:** Our web app employs advanced transfer learning models to accurately identify the type of disease affecting plants. Users can upload images of afflicted plants for real-time diagnosis.

- **Treatment Recommendations:** Beyond disease identification, the app provides actionable insights by recommending suitable treatments for the detected diseases. This feature aids farmers and agricultural practitioners in promptly addressing plant health issues.

- **Prevention Suggestions:** The application doesn't stop at diagnosis; it also offers preventive measures to curb the spread of diseases. Users receive valuable suggestions on maintaining plant health and preventing future infections.

- **Generative AI Interaction:** To enhance user experience, we've integrated generative AI capabilities for handling additional questions users may have about their plants. This interactive feature provides users with insightful information and guidance.

## How it Works ?

- **Image Upload:** Users upload images of plant specimens showing signs of disease through the web interface.
- **Transfer Learning Model:** The uploaded images undergo real-time analysis using advanced transfer learning model, enabling the accurate identification of diseases with the help of PlantID API.
- **Treatment and Prevention Recommendations:** Once the disease is identified, the web app provides detailed information on suitable treatments and preventive measures, empowering users with actionable insights.
- **Generative AI Interaction:** Users can engage with generative AI to seek additional information, ask questions, or gain knowledge about plant care beyond disease diagnosis.

## Setup and Deployment
1. **Clone the repository**
  
```terminal
git clone https://github.com/kashish1928/Plant-Disease-Detection.git
```

2. **Navigate to project directory**

```terminal
cd Plant-Disease-Detection
```

3. **Install dependencies**

```terminal
pip install -r requirements.txt
```

4. **Run the program**

```terminal
python src/main.py
```

5. **Access the webapp**

Open a web browser and go to `http://127.0.0.1:5001/`

## Packages Used

|Package Name|Version|
|--------------|--------------|
|matplotlib|3.8.2|
|openai|1.3.7|
|pillow|10.2.0|
|pymongo|4.6.1|
|python|3.11.4|
|taipy|3.0.0|

## Technologies Used


- ![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
- Taipy
- ![image](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
- GPT 3
- ![image](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)


Feel free to explore, contribute, and enhance the capabilities of our Plant Whisperer Application. Together, let's empower farmers and agricultural stakeholders with cutting-edge technology for sustainable crop management.

## License Information  
The software provided in this project is offered under the [MIT](https://opensource.org/license/mit/) open source license and [CC-BY](https://creativecommons.org/about/cclicenses/#:~:text=CC%20BY%3A%20This%20license%20allows,license%20allows%20for%20commercial%20use.). See [LICENSE.md](LICENSE.md) for more information.
