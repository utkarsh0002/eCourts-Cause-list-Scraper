# 🏛️ eCourts Cause List Scraper (Manual Captcha)

A **Python Selenium-based web scraper** that extracts **district court cause list data** from the official [eCourts India portal](https://services.ecourts.gov.in/) and exports it into a **beautifully formatted PDF** using `reportlab`.

---

## 📋 Overview

This project automates the retrieval of **daily cause lists** (case schedules) from district courts available on the eCourts website.

Since the portal uses a **CAPTCHA**, the scraping process is **semi-automatic** — the user performs the search manually, and the script takes over to extract and structure the case data into a local PDF file.

---

## ⚙️ Features

✅ Extracts all cases from the cause list table (after manual captcha input)  
✅ Cleans and formats messy case text  
✅ Skips section headers like *“Urgent Cases”* or *“Time Bound”*  
✅ Generates a **well-structured, professional PDF**  
✅ No external dependencies beyond Selenium and ReportLab  

---

## 🧠 Workflow

1. The script launches the **eCourts cause list page** in Chrome.
2. You manually:
   - Select *State*, *District*, *Court*, and *Date*
   - Fill the *CAPTCHA*
   - Click **"View Cause List"**
3. Once the table is fully loaded, you press **Enter** in the console.
4. The program scrapes all case details and saves them into a **formatted PDF file** (`Cause_List.pdf`).

---

## 🧩 Data Extracted

Each case entry in the PDF includes:
- **Sr No**
- **Case Info** (e.g. “SUIT/109794/1999”, “Next hearing date:- 15-10-2025”)
- **Party Name**
- **Advocate(s)**

---

## 🛠️ Installation

Clone the repository and install the required Python dependencies:

```bash
git clone https://github.com/utkarsh0002/eCourts-Cause-List-Scraper.git
cd eCourts-Cause-List-Scraper
pip install selenium webdriver-manager reportlab
```

---

## ▶️ Usage

Run the scraper directly from the terminal:

```bash
python ecourts_cause_list_scraper.py
```

Follow the console instructions:

1. Wait for the browser window to open.  
2. Manually select **State**, **District**, **Court**, and **Date**.  
3. Fill the **CAPTCHA** and click **"View Cause List"**.  
4. Once the table loads completely, return to the console and press **Enter**.  

After the process completes, a formatted PDF (**Cause_List.pdf**) will be created in the same directory.

---

## 📄 Output Example

**Sample PDF Table Layout:**

| Sr No | Case Info | Party Name | Advocate |
|-------|------------|-------------|-----------|
| 1 | SUIT/109794/1999 — Next hearing date: 15-10-2025 | Suresh Ramchand Mehta (Targeted Matter) versus Galaxy Corporation | Kudalkar S M ASSOCIATES, Vijay B Mishra |

---

## 🧰 Tech Stack

- **Python 3.x**
- **Selenium** → Browser automation  
- **ReportLab** → PDF generation  
- **Webdriver-Manager** → Automatically installs and manages ChromeDriver  

---

## 📦 Project Structure

eCourts-Cause-List-Scraper/  
│  
├── ecourts_cause_list_scraper.py # Main scraper script  
├── Cause_List.pdf # Example generated PDF  
└── README.md # Project documentation  

---

## ⚠️ Notes

- This scraper works **semi-automatically** because the eCourts portal uses CAPTCHA.  
- You must fill the CAPTCHA manually and wait for the table to fully load before pressing **Enter**.  
- Designed specifically for **district court cause lists** on the eCourts India portal.  
- Make sure your **internet connection** and **Chrome browser** are stable and updated.  
- The generated PDF is saved in the same directory as the script.  

---

## 👨‍💻 Author

Utkarsh Vats  
B.Tech (2024–2028)  

