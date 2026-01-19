import requests

RESOURCES = {
    "Logistics Manager": [
        ("Coursera: Supply Chain Management (Rutgers/Google)", "https://www.coursera.org/search?query=supply%20chain%20management"),
        ("edX: Supply Chain MicroMasters (MIT)", "https://www.edx.org/school/mitx"),
        ("ASCM: CSCP Certification (Official)", "https://www.ascm.org/learning-development/certifications-credentials/cscp/"),
        ("IEEE Xplore: Semiconductor Logistics", "https://ieeexplore.ieee.org/Xplore/home.jsp"),
        ("LinkedIn Learning: Logistics & Supply Chain", "https://www.linkedin.com/learning/topics/logistics-and-supply-chain-management"),
    ],
    "Supply Chain Analyst": [
        ("Coursera: Supply Chain Analytics", "https://www.coursera.org/search?query=supply%20chain%20analytics"),
        ("MIT OpenCourseWare: Supply Chain", "https://ocw.mit.edu/search/?q=supply+chain"),
        ("Gartner: Supply Chain Insight", "https://www.gartner.com/en/supply-chain"),
        ("Udemy: Supply Chain Data Science", "https://www.udemy.com/courses/business/Data-and-Analytics/"),
        ("ASCM: CPIM Certification (Official)", "https://www.ascm.org/learning-development/certifications-credentials/cpim/"),
    ],
    "Warehouse Supervisor": [
        ("LinkedIn Learning: Warehouse Management", "https://www.linkedin.com/learning/topics/warehouse-management"),
        ("Coursera: Warehouse Operations", "https://www.coursera.org/search?query=warehouse%20management"),
        ("OSHA: Warehousing Safety Standards", "https://www.osha.gov/warehousing"),
        ("WERC: Warehousing Education & Research", "https://werc.org/"),
        ("ASCM: Principles of Inventory Management", "https://www.ascm.org/learning-development/certificates/inventory-management/"),
    ],
    "Procurement Specialist": [
        ("Coursera: Procurement & Sourcing", "https://www.coursera.org/search?query=procurement"),
        ("CIPS: Global Standard for Procurement", "https://www.cips.org/"),
        ("SIA: Semiconductor Industry Resources", "https://www.semiconductors.org/"),
        ("LinkedIn Learning: Strategic Sourcing", "https://www.linkedin.com/learning/topics/procurement"),
        ("Harvard Online: Negotiation", "https://online.hbs.edu/subjects/negotiation/"),
    ]
}

print("Validating Resource Links...")
print("-" * 60)

headers = {'User-Agent': 'Mozilla/5.0'}

for role, links in RESOURCES.items():
    print(f"\nChecking ROLE: {role}")
    for title, url in links:
        try:
            r = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            if r.status_code == 405: # Some sites block HEAD
                r = requests.get(url, headers=headers, timeout=5, stream=True)
            
            status = "OK" if r.status_code < 400 else f"FAIL ({r.status_code})"
            print(f"[{status}] {title}\n      {url}")
        except Exception as e:
            print(f"[ERROR] {title}: {str(e)}")
