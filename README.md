

# 🎓 Global University Explorer Dashboard

An interactive Streamlit web application designed to explore, compare, and visualize global university data, powered by comprehensive institution details and QS World University Rankings 2025.

---

## ✨ Project Description

This project provides a dynamic and user-friendly platform for delving into university information worldwide. Whether you're a prospective student, researcher, or an educational advisor, this dashboard aims to simplify the process of discovering, analyzing, and comparing higher education institutions based on their general details and performance in the QS World University Rankings 2025.

---

## 🚀 Features

* **Comprehensive University Explorer:**
    * **Interactive Filters:** Easily narrow down your search using filters for Country, State/Province, and a search bar for University Name.
    * **Top 5 QS Universities:** Highlights the top 5 QS-ranked universities within a selected country for quick reference.
    * **Detailed University Cards:** Presents filtered universities with essential information such as location, academic domains, and direct website links.
    * **Data Export:** Allows users to download the currently filtered university data as a CSV file.

* **⚖️ University Comparison Tool:**
    * **Side-by-Side Analysis:** Select up to three QS-ranked universities for a direct, side-by-side comparison of their key attributes.
    * **Key Comparison Metrics:** Compares details like country, state/province, websites, domains, and all available QS Ranking metrics (Overall Score, Academic Reputation Score, Employer Reputation Score).

* **📊 Statistical Visualizations:**
    * **Geographical Insights:** Visualizes the top 10 countries with the highest number of universities.
    * **Domain Trends:** Displays the top 10 most common academic domains across universities.
    * **Filtered Data Metrics:** Provides a summary of the total number of universities matching the active filters.

---

## ⚙️ How to Set Up and Run Locally

Follow these steps to get the Global University Explorer Dashboard running on your local machine.

### Prerequisites

* Python 3.7+
* `pip` (Python package installer)

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository_url>
cd study-abroad-dashboard
```
*(Replace `<repository_url>` with the actual URL of your Git repository.)*

### 2. Place Data Files

Ensure you have the necessary CSV data files in the root directory of your project:

* `list_of_univs.csv`
* `QS World University Rankings 2025 (Top global universities).csv`

### 3. Install Dependencies

Install all required Python packages using pip:

```bash
pip install -r requirements.txt
```
*(If you don't have a `requirements.txt` file, you can create one manually with the following content, then run `pip install -r requirements.txt`)*:

```
streamlit
pandas
streamlit-tags
```

### 4. Run the Streamlit App

Navigate to the project root directory in your terminal and run the app:

```bash
streamlit run app.py
```

Your web browser should automatically open the Streamlit application. If not, open your browser and navigate to `http://localhost:8501`.

---

## 📂 Project Structure

```
study-abroad-dashboard/
├── app.py                      # Main Streamlit application file
├── list_of_univs.csv           # General university data
├── QS World University Rankings 2025 (Top global universities).csv # QS Ranking data
└── requirements.txt            # List of Python dependencies
```

---

## 📸 Screenshots

![image](https://github.com/user-attachments/assets/b7004767-6b7f-46aa-b6cb-0707083a6511)


![image](https://github.com/user-attachments/assets/990aa3fb-7da6-47dc-8fbc-aa70d11ff96e)

![image](https://github.com/user-attachments/assets/ad85286d-d7ea-4a61-b451-84ca19e1a1d3)


## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

---

## 📧 Contact

If you have any questions or feedback, please feel free to reach out.

---
