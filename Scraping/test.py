import pdfquery
import pandas as pd

pdf = pdfquery.PDFQuery('SAT.pdf')
print(pdf);
pdf.load()
pdf.tree.write('pdfXML.txt', pretty_print = True)
print()

def pdfscrape(pdf):
    # Extract each relevant information individually
    ssn              = pdf.pq('LTTextLineHorizontal:overlaps_bbox("47.2, 572.342, 526.56, 580.342")').text()
    employer_name    = pdf.pq('LTTextLineHorizontal:overlaps_bbox("47.2, 550.342, 221.56, 558.342")').text()
    #employer_address = pdf.pq('LTTextLineHorizontal:overlaps_bbox("517.24, 465.342, 564.8, 473.342)').text()
    first_name       = pdf.pq('LTTextLineHorizontal:overlaps_bbox("47.2, 272.342, 562.76, 280.342")').text()
    last_name        = pdf.pq('LTTextLineHorizontal:overlaps_bbox("437.98, 648.342, 460.484, 656.342")').text()
    employee_address = pdf.pq('LTTextLineHorizontal:overlaps_bbox("151.52, 465.342, 197.248, 473.342")').text()
    medicare_wage_tip= pdf.pq('LTTextLineHorizontal:overlaps_bbox("47.2, 717.35, 147.52, 750.0")').text()
# Combined all relevant information into single observation
    page = pd.DataFrame({
                         'ssn': ssn,
                         'employer_name': employer_name,
                         #'employer_address': employer_address,
                         'first_name': first_name,
                         'last_name': last_name,
                         'employee_address': employee_address,
                         'medicare_wage_tip': medicare_wage_tip
                       }, index=[0])
    return(page)

pagecount = pdf.doc.catalog['Pages'].resolve()['Count']
master = pd.DataFrame()
for p in range(pagecount):
    pdf.load(p)
    page = pdfscrape(pdf) 
    master = master.append(page, ignore_index=True)
    
master.to_csv('output.csv', index = False)