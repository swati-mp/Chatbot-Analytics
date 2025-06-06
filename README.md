# Chatbot Analytics Dashboard

A secure, interactive dashboard built with **Streamlit** to track and visualize chatbot user interactions.
This dashboard provides key metrics such as total queries, most common conversation topics, and user satisfaction ratings over time. It also allows logging new chatbot interactions in real-time.

---

## Features

* Password-protected access for security
* Displays key metrics:

  * Total number of interactions
  * Average satisfaction rating
  * Number of unique conversation topics
* Visualizes:

  * Topic distribution as a bar chart
  * Satisfaction ratings trend over time as a line chart
* Form to log new interactions directly into the SQLite database

---

## Tech Stack

* Python
* Streamlit (for UI)
* SQLite (for data storage)
* Pandas (for data manipulation)
* Plotly Express (for interactive charts)

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/chatbot-analytics.git
   cd chatbot-analytics
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install streamlit pandas plotly sqlite3
   ```

4. **Prepare the SQLite database**

   * Create an SQLite database file named `analytics.db`
   * Create the `interactions` table with the following schema:

     ```sql
     CREATE TABLE interactions (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       topic TEXT NOT NULL,
       rating REAL NOT NULL
     );
     ```

5. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**

   * Open the URL shown in the terminal (usually `http://localhost:8501`)
   * Enter the password (`admin123` by default) to access the analytics dashboard

---

## Usage

* View chatbot interaction metrics and charts on the dashboard
* Log new interactions by entering a topic and satisfaction rating using the form at the bottom
* Data is stored persistently in the SQLite database

---

## Security

* Basic password protection implemented
* Change the `PASSWORD` variable in `app.py` to secure your dashboard

---

## Future Improvements

* Add user authentication and roles
* Support export of analytics data (CSV, Excel)
* Add more detailed interaction metadata (timestamps, user IDs)
* Implement dashboard filters by date or topic
