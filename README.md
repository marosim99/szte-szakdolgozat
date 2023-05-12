# szte-szakdolgozat
Marosi Márk Dániel, SZTE TTIK Gazdaságinformatikus szakos hallgató szakdolgozata.

Az applikáció indításához a card_digitizer.py fájl main metódusát kell futtatni.

A test_images mappában találhatóak képek, melyekre tesztelhető az alkalmazás.

A Research mappában található pytesseract_test.py futtatásához telepíteni szükséges a Tesseract OCR-t innen: https://tesseract-ocr.github.io/tessdoc/Downloads.html

A telepítés végeztével meg kell adnunk a tesseract.exe elérési útvonalát a pytesseract_test.py fájlban az alábbi módon:

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'