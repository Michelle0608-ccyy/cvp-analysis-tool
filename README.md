#  CVP (Cost-Volume-Profit) Analysis Tool

##  Project Introduction

This is an interactive web application developed for the managment accounting, built with the Streamlit framework. The tool is designed to automate Cost-Volume-Profit (CVP) analysis, a core management accounting method for corporate profit forecasting, break-even point calculation, cost structure optimization, and supporting business making decisions.

Users can input core business parameters by themselves through the sidebar, and the tool will automatically complete the calculation of key indicators, visual chart plotting, industry benchmark comparison, and targeted strategic recommendation output. It helps users quickly complete professional CVP analysis without complex manual formula operations.

##  Core Features

1.  **Customizable Parameter Input**: Sidebar interactive input for core business parameters, including Fixed Cost (FC), Selling Price per Unit (SP), Variable Cost per Unit (VC), and sales volume range setting.
2.  **Fully Automatic CVP Core Calculation**: Calculation of unit contribution margin in real time, contribution margin ratio, break-even sales volume, break-even revenue, and other core CVP indicators.
3.  **Industry Benchmark Comparison Module**: Industry average financial indicators from 2023 to 2025, covering Manufacturing, Service Industry and Technology Industry, supporting comparison between corporate indicators and industry benchmarks.
4.  **Professional Visual Analysis Chart**: Automatically generate a standard CVP analysis chart, including total revenue line, total cost line, fixed cost line, break-even point mark, profit and loss area filling, and dynamic industry benchmark reference line.
5.  **Detailed Data Table**: Output a complete data table of revenue, cost and profit under different sales volumes, supporting full data traceability.
6.  **Intelligent Analysis and Strategic Recommendation**: Automatically judge business status based on input parameters, and output targeted, actionable strategic optimization recommendations.

## How to Run the Application

### Prerequisites
Please make sure you have Python 3.8 or above installed on your device.

### Step 1: Download the Project from GitHub
Visit the project repository at https://github.com/Michelle0608-ccyy/cvp-analysis-tool. Click the green "Code" button, then select "Download ZIP" to save the compressed file to your computer.

### Step 2: Extract and Prepare the Folder
Extract the downloaded ZIP file. A folder named cvp-analysis-tool will be created automatically. Move this folder to your Desktop for easy access.

### Step 3: Open the Command Line in the Project Folder
Choose one of the following methods to open Command Prompt directly in the project folder:
#### Method 1 (Using commands):
Open Command Prompt, then run these two commands in sequence:
```bash
cd Desktop
```
```bash
cd cvp-analysis-tool
```
#### Method 2 (Faster option):
Open the cvp-analysis-tool folder on your Desktop, type cmd in the address bar at the top of the window, then press Enter. This will launch Command Prompt already located in the project folder.

### Step4: Install Dependencies and Launch the Application
First, install all required libraries using the included requirements.txt file:
```bash
pip install -r requirements.txt
```
3. Run the application with the following command:
```bash
streamlit run app.py
```
If you encounter a command error on Windows, use this compatible command instead:
```bash
python -m streamlit run app.py
```
The application will automatically launch in your default browser, and you can start the CVP analysis immediately.

In step 4, if the first method fails, you can install the required libraries one by one with the following commands:
```bash
pip install streamlit
pip install pandas
pip install numpy
pip install matplotlib
```
or choose this approach below, which can achieve the installation of all the above libraries at one time.
```bash
pip install streamlit pandas numpy matplotlib
```
Then run the application:
```bash
streamlit run app.py
# Windows compatible command
# python -m streamlit run app.py
```
## Data Sources
The 2023-2025 industry average financial indicators built in this tool are for academic assignment demonstration only, and the data sources are:

Yahoo Finance Global Industry Financial Database (2023-2025): https://finance.yahoo.com/industries

National Bureau of Statistics of China Open Government Data (2023-2025): https://www.stats.gov.cn/english

All data are real industry statistics, traceable through the above official channels.

## Project File Structure
```bash
cvp-analysis-tool/
├── app.py                 # Core code of the CVP analysis application, including all calculation logic and page design
├── requirements.txt       # Dependency library list of the project
└── README.md              # Project description document (this file)
```
## Author Information
**Name**: Ziyou Liao

**Student ID**: 2471574

**Submission Date**: 23th, April 2026
