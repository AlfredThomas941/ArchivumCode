# ArchivumCode
# 📄 PDF-Barcode-Tagger  

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)  
![Status](https://img.shields.io/badge/status-pre--alpha-orange.svg)  
![License](https://img.shields.io/badge/license-proprietary-red.svg)  

A lightweight Python tool to **add unique barcodes to every page of a PDF**, while intelligently avoiding text and images.  
Ideal for **libraries, archives, and document management systems**.  

---

## ✨ Features  

✅ **Automatic Barcode Placement**  
Generates **Code128 barcodes** for each page.  

✅ **Smart Content-Aware Placement**  
Scans each page for text/images and avoids overlapping them.  

✅ **Auto-Incrementing Unique IDs**  
Uses **date + category + running page number** to generate unique IDs.  

✅ **Category Support**  
Lets you group barcodes into **1–4 categories**.  

✅ **Last Barcode Memory**  
Saves the **last used barcode ID** so it continues seamlessly.  

✅ **Safe PDF Handling**  
Creates a new **barcoded_<filename>.pdf** without modifying your original.  

✅ **Works With Any PDF**  
Handles **scanned, text-based, or mixed PDFs**.  

---

## 📦 Installation  

1️⃣ **Clone this repo**  
```bash
git clone https://github.com/AlfredThomas941/ArchivumCode.git
cd ArchivumCode
```

2️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage  

Run the script:  

```bash
python barcode_adder.py
```

You’ll be asked for:  

- 📄 **PDF file path**  
- 🏷️ **Category (1–4)**  
- 🔢 **Starting number (optional)**  

**Output:**  

- ✅ A **new PDF** → `barcoded_<originalfile>.pdf`  
- ✅ A **log file** → `last_barcode.txt` (remembers last used barcode)  

---

## 🛠 Requirements  

- Python **3.8+**  
- Libraries:  

```text
python-barcode
pillow
pypdf2
reportlab
pdfminer.six
```

Install all at once:  

```bash
pip install python-barcode pillow pypdf2 reportlab pdfminer.six
```

---

## 🔢 Barcode Numbering Explained  

Each barcode ID is generated as:  

```
DDMM(last digit of year)(Category)(Page Number)
```

📌 **Example:**  

- **Date:** 27 July 2025 → `2707`  
- **Year last digit:** `5`  
- **Category:** `2`  
- **Page number:** `012`  

✅ **Final Barcode → 270752012**  

It **auto-increments per page** and **resumes from last saved barcode** next time.  

---

## 📂 Project Structure  

```
PDF-Barcode-Tagger/
│
├── gitignore           # Ignored files
├── LICENSE              # Proprietary license 
├── README.md            # Project documentation  
├── barcode_adder.py     # Main script
└── requirements.txt     # Dependencies
```

---

## 🔮 Roadmap  

Planned future updates:  

- [] **QR Code Support** → Store metadata or URLs  
- [ ] **Database Logging** → Track barcode → page mapping  
- [ ] **Barcode Scanner Tool** → Fetch page instantly  
- [ ] **Custom Placement Modes** → Always bottom-right, fixed position  
- [ ] **Drag & Drop GUI** → Easier use for non-technical users  
- [ ] **Support More Barcode Formats** → Code39, EAN, etc.  

---

## 📜 License  

**Proprietary License**  

This software is for **personal/private use only**.  
No redistribution, modification, or commercial use is allowed without permission.  

See [LICENSE] file for details.  

---

## 📨 Contact  

📧 For inquiries or permissions, contact on **alfredthomas941@gmail.com**.  
