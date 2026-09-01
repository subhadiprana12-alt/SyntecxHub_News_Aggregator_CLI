# 📰 SyntecxHub News Aggregator CLI

A simple and beginner-friendly **News Aggregator CLI** built using Python.

This project collects news headings from selected news websites using web scraping, stores the collected data in an SQLite database, and provides options to search, filter, and export the news.

## 🚀 Features

* 🌐 Fetch news headings from news websites
* 🗄️ Store collected news in SQLite
* 🔍 Search news by keyword
* 📰 Filter news by source
* 📅 Filter news by date
* ♻️ Remove duplicate headlines
* 📄 Export news to JSON
* 📊 Export news to CSV
* 📗 Export news to Excel
* 💻 Simple command-line interface

## 🛠️ Technologies Used

* **Python** – Main programming language
* **Requests** – Fetches webpage content
* **BeautifulSoup** – Extracts headings from webpages
* **SQLite3** – Stores the collected news
* **Pandas** – Handles and exports the data
* **JSON** – JSON file export
* **OpenPyXL** – Excel file export

## 📁 Project Structure

```text
SyntecxHub_News_Aggregator_CLI/
│
├── main.py
├── requirements.txt
├── README.md
│
├── news.db
├── news.json
├── news.csv
└── news.xlsx
```

> `news.db`, `news.json`, `news.csv`, and `news.xlsx` are generated when the program is used.

## ⚙️ Installation

### 1. Open the Project

Download or clone the repository and open the project folder in VS Code or any preferred code editor.

### 2. Install Required Libraries

Open the terminal inside the project folder and run:

```bash
pip install -r requirements.txt
```

You can also install the libraries manually:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## ▶️ Run the Project

Run the following command:

```bash
python main.py
```

The program will display the following menu:

```text
========================================
          NEWS AGGREGATOR
========================================

1. Collect News
2. Show All News
3. Search by Keyword
4. Filter by Source
5. Filter by Date
6. Export News
7. Exit
```

## 📌 How It Works

### 1. Collect News

Select:

```text
1
```

The program sends a request to the configured news websites and uses BeautifulSoup to extract the available news headings.

The collected information is then stored in the SQLite database.

Example:

```text
Collecting news...

BBC: XX headings found

Total unique articles: XX
New articles saved: XX
```

The number of headings may change because news websites are regularly updated.

### 2. Show All News

Select:

```text
2
```

This displays the news stored in the database.

Example:

```text
Title : Example News Headline
Source: BBC
Date  : 2026-09-01
Link  : https://www.bbc.com/...
```

### 3. Search by Keyword

Select:

```text
3
```

Enter a keyword.

Example:

```text
Enter keyword: India
```

The program searches the stored headlines and displays matching results.

### 4. Filter by Source

Select:

```text
4
```

Enter the name of a news source.

Example:

```text
Enter source: BBC
```

Only news from the selected source will be displayed.

### 5. Filter by Date

Select:

```text
5
```

Enter a date in the following format:

```text
YYYY-MM-DD
```

Example:

```text
Enter date: 2026-09-01
```

The program displays news collected on that date.

### 6. Export News

Select:

```text
6
```

The program provides three export options:

```text
1. JSON
2. CSV
3. Excel
```

Depending on the selected option, the program creates:

```text
news.json
news.csv
news.xlsx
```

These files can be opened and used for further analysis.

### 7. Exit

Select:

```text
7
```

to close the application.

## 🌐 Adding Another News Website

The project uses a reusable scraping function, so another website can be added by providing its URL, source name, and base URL.

Example:

```python
new_news = get_news(
    "https://example.com/news",
    "Example News",
    "https://example.com"
)

all_news += new_news
```

Different websites may have different HTML structures. Therefore, some websites may require changes to the scraping logic.

## 🗃️ Database

The project uses **SQLite** to store the collected news.

Each news record contains:

| Field  | Description                      |
| ------ | -------------------------------- |
| ID     | Unique ID of the news            |
| Title  | News headline                    |
| Source | News website                     |
| Link   | Article link                     |
| Date   | Date when the news was collected |

The database file is:

```text
news.db
```

## 🔄 Project Workflow

```text
News Website
      ↓
Requests
      ↓
BeautifulSoup
      ↓
Extract Headings
      ↓
Remove Duplicates
      ↓
SQLite Database
      ↓
Search / Filter
      ↓
JSON / CSV / Excel
```

## 🎯 Project Objective

The main objective of this project is to demonstrate the practical use of Python for:

* Web scraping
* Data collection
* Data storage
* Searching and filtering
* Duplicate handling
* CSV and Excel automation
* JSON data export
* Building a command-line application

## ⚠️ Note

The HTML structure of websites can change over time. If a website changes its structure, the scraping logic may need to be updated.

This project is created for **educational purposes** and should be used responsibly while respecting the terms and policies of the websites being accessed.

## 👨‍💻 Author

**Subhadip Rana**

GitHub:
https://github.com/subhadiprana12-alt/SyntecxHub_News_Aggregator_CLI

## 📌 Project

**SyntecxHub News Aggregator CLI**

Built with ❤️ using Python.
