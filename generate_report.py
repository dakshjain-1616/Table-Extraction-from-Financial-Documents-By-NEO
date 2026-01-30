import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_financial_report(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Annual Financial Report 2025", styles['Title']))
    elements.append(Spacer(1, 12))

    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['Heading2']))
    elements.append(Paragraph(
        "This report provides a comprehensive overview of the financial performance of the "
        "organization for the fiscal year 2025. Key highlights include significant growth in "
        "revenue and optimization of operating expenses.", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Balance Sheet Table
    elements.append(Paragraph("Consolidated Balance Sheet", styles['Heading3']))
    data = [
        ['Category', '2025 (USD)', '2024 (USD)'],
        ['Total Assets', '15,200,000', '13,500,000'],
        ['Total Liabilities', '6,800,000', '6,200,000'],
        ['Shareholder Equity', '8,400,000', '7,300,000'],
        ['Net Income', '2,100,000', '1,850,000'],
    ]
    
    table = Table(data, colWidths=[200, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Note section
    elements.append(Paragraph("Notes to Financial Statements", styles['Heading3']))
    elements.append(Paragraph(
        "1. Revenue recognition is based on completion of service milestones.<br/>"
        "2. Depreciation is calculated using the straight-line method over 5 years.", styles['Normal']))

    doc.build(elements)
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    report_path = "/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/data/raw/financial_report.pdf"
    generate_financial_report(report_path)