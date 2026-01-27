# Water Quality Chatbot - Overview

## What is it?

The Water Quality Chatbot is a simple tool that lets you ask questions about water monitoring data in plain English. Instead of manually searching through spreadsheets or writing complex formulas, you just type a question like "What was the coldest water temperature in January?" and get an instant answer.

## Who is it for?

Researchers, field technicians, and team members who work with water quality data but don't want to spend time digging through Excel files or learning data analysis software.

## How does it work?

1. **You upload your Excel file** (It also can accept NetCDF file format) containing water quality measurements (temperature, dissolved oxygen, bacteria levels, pH, etc.)

2. **You ask questions in everyday language** — for example:
   - "Show me all data from site 2"
   - "Compare summer vs winter dissolved oxygen"
   - "What's the average pH by year?"

3. **The app understands your question** by recognizing key words (like "average", "compare", "trend") and matching them to the right data columns

4. **You get results instantly** — displayed as tables, statistics, or summaries right in your browser

The app also lets you export your data to NetCDF format, which is commonly used by scientists and GIS software for environmental analysis.

## What makes it different?

- **No internet required** — runs entirely on your computer
- **No subscription fees** — completely free to use
- **No coding needed** — just type questions like you're asking a colleague
- **Remembers your data** — upload once, query anytime

## Technical Background

The app is built with **Python**, using **Streamlit** for the web interface and **Pandas** for data processing. It uses pattern matching (**not AI**) to interpret questions, which means it works offline and costs nothing to run.

---

*Built for watershed monitoring research teams who want quick answers from their data.*
