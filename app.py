import io
import os
from datetime import datetime

import markdown2
import streamlit as st

try:
    import pdfkit
except ImportError:
    pdfkit = None

st.set_page_config(page_title="Mehfil Meeting Report", page_icon="📄", layout="centered")

st.title("AI-Powered Meeting Transcript Summariser")
st.caption("Mehfil Event Planners · Task 5: Generate a downloadable PDF report")

SAMPLE_SUMMARY = """The meeting focused on finalising arrangements for the upcoming wedding event.

Key decisions:
- The event will take place at the selected venue on the agreed date.
- The décor team will use the approved colour palette and stage layout.
- Catering will prepare the confirmed menu and finalise the guest count.
- The event coordinator will circulate the updated schedule to all vendors.

Action items:
- Venue team: confirm the final floor plan.
- Décor team: share the revised design proposal.
- Catering team: submit the final menu and guest estimate.
- Event coordinator: distribute the consolidated event schedule."""

DEFAULT_CHECKLIST = [
    ("Key decisions are clearly stated", True),
    ("Action items identify an owner", True),
    ("Important dates and deadlines are included", False),
    ("Unconfirmed details are marked for follow-up", True),
]

def build_markdown(summary: str, checklist: list[tuple[str, bool]]) -> str:
    rows = "\n".join(
        f"| {item.replace('|', r'\\|')} | {'Complete' if done else 'Pending'} |"
        for item, done in checklist
    )
    return f"""# Meeting Report

**Client:** Mehfil Event Planners  
**Generated:** {datetime.now().strftime('%d %B %Y, %I:%M %p')}

## Summary

{summary.strip()}

## Checklist

| Review item | Status |
|---|---|
{rows}

---
*Prepared using the Mehfil Event Planners meeting report tool.*
"""

def html_document(markdown_text: str) -> str:
    body = markdown2.markdown(
        markdown_text,
        extras=["tables", "fenced-code-blocks", "smarty-pants"]
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 22mm 18mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; color: #243247; font-size: 11pt; line-height: 1.55; }}
h1 {{ color: #17365d; font-size: 24pt; border-bottom: 2px solid #d6e2f0; padding-bottom: 8px; }}
h2 {{ color: #1f4e79; font-size: 16pt; margin-top: 24px; }}
p {{ margin: 8px 0; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
th {{ background: #17365d; color: white; text-align: left; }}
th, td {{ border: 1px solid #cbd5e1; padding: 9px; }}
tr:nth-child(even) {{ background: #f3f6fa; }}
li {{ margin-bottom: 5px; }}
</style></head><body>{body}</body></html>"""

def make_pdf(html: str) -> bytes:
    """Create a PDF with pdfkit/wkhtmltopdf; use ReportLab as a local fallback."""
    if pdfkit is not None:
        configured_path = os.environ.get("WKHTMLTOPDF_PATH")
        try:
            config = pdfkit.configuration(wkhtmltopdf=configured_path) if configured_path else None
            options = {"encoding": "UTF-8", "page-size": "A4", "margin-top": "18mm",
                       "margin-right": "18mm", "margin-bottom": "18mm", "margin-left": "18mm"}
            pdf_bytes = pdfkit.from_string(html, False, options=options, configuration=config)
            if pdf_bytes:
                return pdf_bytes
        except Exception:
            pass

    # Fallback keeps the app usable in environments where wkhtmltopdf is unavailable.
    from xhtml2pdf import pisa
    output = io.BytesIO()
    result = pisa.CreatePDF(io.StringIO(html), dest=output, encoding="utf-8")
    if result.err:
        raise RuntimeError("PDF generation failed. Check the PDF dependencies.")
    return output.getvalue()

with st.expander("Sample meeting transcript", expanded=False):
    st.text_area(
        "Example transcript",
        value=("Coordinator: The wedding is scheduled for 18 December. The venue team will confirm "
               "the floor plan by Friday. The client approved the ivory and gold décor. Catering "
               "will provide the final menu and guest estimate by Monday. The coordinator will "
               "send the updated vendor schedule after receiving all confirmations."),
        height=130,
        disabled=True,
    )

st.subheader("Meeting summary")
summary = st.text_area(
    "Enter or paste the complete meeting summary",
    value=SAMPLE_SUMMARY,
    height=260,
    help="Paste the summary produced by the earlier summarisation task. The full text is included in the PDF."
)

st.subheader("Summary quality checklist")
st.caption("Update each item before generating the report.")
checklist_items = []
for index, (label, default_status) in enumerate(DEFAULT_CHECKLIST):
    left, right = st.columns([4, 1])
    with left:
        item = st.text_input(f"Checklist item {index + 1}", value=label, key=f"item_{index}")
    with right:
        done = st.selectbox("Status", ["Complete", "Pending"], index=0 if default_status else 1,
                            key=f"status_{index}", label_visibility="visible")
    checklist_items.append((item, done == "Complete"))

markdown_report = build_markdown(summary, checklist_items)
with st.expander("Preview report Markdown"):
    st.markdown(markdown_report)

if not summary.strip():
    st.warning("Enter a summary before generating the PDF.")
else:
    try:
        html = html_document(markdown_report)
        pdf_buffer = io.BytesIO(make_pdf(html))
        pdf_buffer.seek(0)
        st.download_button(
            label="Download Report",
            data=pdf_buffer,
            file_name="meeting_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as error:
        st.error(f"Could not generate the PDF: {error}")
        st.info("Install the dependencies listed in requirements.txt and, if needed, wkhtmltopdf.")
