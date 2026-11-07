# Mehfil Event Planners — Meeting Report Generator (Task 5)

A Streamlit application that combines a meeting summary and its quality checklist into a Markdown report, converts the Markdown to HTML with `markdown2`, generates a PDF, and provides a **Download Report** button. The downloaded file is named `meeting_report.pdf`.

## Features

- Editable meeting summary with the complete text included in the report.
- Editable checklist items with `Complete` / `Pending` status.
- Markdown report preview.
- PDF download as `meeting_report.pdf`.
- PDF generation through `pdfkit` + `wkhtmltopdf`; an `xhtml2pdf` fallback is included for environments where the wkhtmltopdf binary is unavailable.

## Project files

```text
.
├── app.py
├── requirements.txt
├── packages.txt
├── sample_transcript.txt
├── sample_summary.md
└── README.md
```

## Run locally (Windows / VS Code)

1. Install Python 3.10 or later.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install Python dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Install the **wkhtmltopdf** Windows installer from the official project download page:
   <https://wkhtmltopdf.org/downloads.html>

6. If its executable is not on PATH, set its location in PowerShell for the current terminal (adjust the path if necessary):

   ```powershell
   $env:WKHTMLTOPDF_PATH = "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
   ```

7. Start the app:

   ```powershell
   streamlit run app.py
   ```

The app opens in your browser. Edit the summary and checklist, then click **Download Report**.

## Deploy to Streamlit Community Cloud

1. Push this repository to a **public** GitHub repository.
2. Sign in to Streamlit Community Cloud and create an app from that repository.
3. Select `app.py` as the main file.
4. Streamlit installs Python packages from `requirements.txt` and system packages from `packages.txt`.
5. After deployment, test the **Download Report** button and confirm the downloaded file opens in a PDF viewer.

`packages.txt` requests the `wkhtmltopdf` system package on the Streamlit Linux environment. The app also includes an `xhtml2pdf` fallback.

## How the report is generated

1. `build_markdown()` combines the complete summary and checklist table.
2. `markdown2.markdown()` converts Markdown into HTML with table support.
3. `pdfkit.from_string()` attempts to create PDF bytes using wkhtmltopdf.
4. If wkhtmltopdf is unavailable, `xhtml2pdf` is used as a fallback.
5. The PDF bytes are placed in an `io.BytesIO` buffer and served by `st.download_button`.

## Task 5 acceptance checklist

- [x] Download button label is **Download Report**.
- [x] Downloaded filename is `meeting_report.pdf`.
- [x] PDF includes a Summary heading and the complete summary text.
- [x] PDF includes a checklist table with item and status columns.
- [x] PDF is generated in memory and served from a buffer.

## Important submission steps

- Make the GitHub repository **public** and submit the repository URL (not your profile URL).
- The internship instructions require at least **3 commits across at least 2 different days**. Make commits on separate days; a ZIP upload alone does not satisfy this requirement.
- Submit the portal note (60+ characters) describing what you implemented, what was difficult, and anything omitted.

## Suggested submission note

Implemented a Streamlit report generator that combines the meeting summary and quality checklist into Markdown, converts it to HTML, and generates a downloadable `meeting_report.pdf`. The main challenge was handling the wkhtmltopdf system dependency across environments, so an xhtml2pdf fallback is included. Live AI transcript summarisation and deployment are outside this Task 5 deliverable.
