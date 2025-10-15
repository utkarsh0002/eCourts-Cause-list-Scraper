"""
eCourts Cause List Scraper (Manual Captcha)
-------------------------------------------
Scrapes district court cause list data case-by-case from the eCourts portal
and exports it as a clean, formatted PDF file.

WORKFLOW:
1. Opens the eCourts "Cause List" page in a browser.
2. User manually selects State, District, Court, Date, and fills captcha.
3. After the table loads, user presses Enter in the console.
4. Script extracts all visible rows from the table, ignoring section headers.
5. Results are saved as a structured, styled PDF.

REQUIREMENTS:
    pip install selenium webdriver-manager reportlab

Author: Utkarsh Vats
Date: 15-10-2025
"""

# ------------------------ Imports ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import time, re

# =========================================================
#                   PDF GENERATION FUNCTION
# =========================================================
def save_cause_list_pdf(data, output_path="cause_list.pdf"):
    """
    Generates a clean, readable PDF file from a list of case data.
    Handles text wrapping, alternating row colors, and formatted headers.

    Args:
        data (list[list]): Nested list where the first row is headers.
        output_path (str): File path for the output PDF.
    """

    # --- Setup PDF Document ---
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),  # landscape for wide tables
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'Wrapped',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        wordWrap='CJK'  # allows wrapping within table cells
    )

    title = Paragraph("<b>District Court Cause List</b>", styles['Title'])
    elements = [title, Spacer(1, 12)]

    # --- Convert each cell to Paragraphs (for wrapping) ---
    wrapped_data = []
    for row_index, row in enumerate(data):
        wrapped_row = []
        for cell in row:
            if row_index == 0:
                # Header row (bold)
                wrapped_row.append(Paragraph(f"<b>{cell}</b>", normal_style))
            else:
                wrapped_row.append(Paragraph(str(cell), normal_style))
        wrapped_data.append(wrapped_row)

    # --- Define Table Layout ---
    table = Table(
        wrapped_data,
        colWidths=[0.6 * inch, 3.2 * inch, 3.5 * inch, 2.8 * inch]
    )

    # --- Apply Styling ---
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),  # header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),            # header text
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f3f3f3")]),                 # alternate row colors
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])

    table.setStyle(style)

    # --- Build and Save PDF ---
    elements.append(table)
    pdf.build(elements)
    print(f"PDF created successfully: {output_path}")


# =========================================================
#                   SELENIUM SCRAPER
# =========================================================

# --- Configure Chrome WebDriver ---
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

# --- Step 1: Open the eCourts Cause List Page ---
driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/index")

print("Please manually select State, District, Court, Date, fill captcha, and click 'View Cause List'.")
input("After the cause list table has fully loaded, press Enter here to continue...")

# --- Step 2: Extract Data from the Cause List Table ---
try:
    table = driver.find_element(By.ID, "dispTable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    data = [["Sr No", "Case Info", "Party Name", "Advocate"]]  # header row

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if not cols:
            continue

        # Skip non-case rows (e.g., section titles like “Urgent Cases”)
        if len(cols) < 4 or any(td.get_attribute("colspan") for td in cols):
            continue

        # --- Extract and clean data ---
        sr_no = cols[0].text.strip()

        # Case info cleanup
        case_text = cols[1].get_attribute("innerText").replace("\n", " ").strip()
        case_text = case_text.replace("\xa0", " ").replace("\u00A0", " ")
        case_text = case_text.replace("View", "").replace("view", "")
        case_text = re.sub(r"['\"]+", "", case_text)
        case_text = re.sub(r"\s{2,}", " ", case_text).strip()
        case_info_clean = case_text

        # Party and advocate names
        party_info = cols[2].get_attribute("innerText").replace("\n", " ").strip()
        advocate = cols[3].get_attribute("innerText").replace("\n", " ").strip()

        data.append([sr_no, case_info_clean, party_info, advocate])

    if len(data) <= 1:
        print("No valid case data found — ensure the table has fully loaded before pressing Enter.")
        driver.quit()

    driver.quit()

except Exception as e:
    print(f"Error reading cause list table: {e}")
    driver.quit()

# --- Step 3: Save Data to PDF ---
save_cause_list_pdf(data, "Cause_List.pdf")
