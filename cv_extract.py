import json

cv_data = {
    "ad_soyad": "FÜRGAN İNCE",
    "profesyonel_unvan": "Junior Data Scientist (Career Transition)",
    "hakkinda": "Electrical & Electronics Engineer transitioning into data science with 4+ years of field execution and quality-control experience in marine projects. Built Python-based tracking and automated reporting workflows to monitor progress, identify delays, and support operational decisions. Completed Miuul Data Scientist Bootcamp and delivered end-to-end analytics and machine learning projects.",
    "iletisim": {
        "telefon": "+90 (531) 703 4594",
        "email": "furganince@outlook.com",
        "konum": "Antalya, Türkiye"
    },
    "teknik_beceriler": {
        "programlama_dilleri": ["Python"],
        "python_kutuphaneleri": ["Pandas", "NumPy", "scikit-learn", "Matplotlib", "Seaborn"],
        "veri_analizi": ["EDA", "Data Cleaning", "Feature Engineering", "Data Wrangling"],
        "makine_ogrenmesi": ["Classification", "Regression", "Clustering", "Model Selection", "Cross-validation", "Hyperparameter Tuning"],
        "veritabani": ["SQL"],
        "evaluasyon_metrikleri": ["ROC-AUC", "PR-AUC", "F1", "Precision/Recall", "Accuracy", "MAE/RMSE"],
        "analiz_araclari": ["A/B Testing", "Hypothesis Testing", "Statistics", "KPI Reporting", "RFM/CLTV", "Association Rules (Apriori)"],
        "arayuzler": ["Power BI", "Excel"],
        "surum_kontrol": ["Git/GitHub"],
        "cekirdek_beceriler": ["Analytical Thinking", "Problem Solving", "Teamwork", "Team Management"]
    },
    "is_deneyimi": [
        {
            "pozisyon": "Field Engineer",
            "sirket": "Bering Yachts",
            "lokasyon": "Antalya, Türkiye",
            "baslangic_tarihi": "11/2024",
            "bitis_tarihi": "11/2025",
            "sorumluluklar": [
                "Tracked project progress and automated reporting in Python, delivering real-time insights on workflow and milestones",
                "Analyzed on-site data to identify delays, optimize resource allocation, and improve operational efficiency",
                "Collaborated with field teams to ensure tasks met standards and timelines, supporting data-driven decisions"
            ]
        },
        {
            "pozisyon": "QA Engineer",
            "sirket": "AGEST Marine Electrical Technologies",
            "lokasyon": "Antalya, Türkiye",
            "baslangic_tarihi": "03/2024",
            "bitis_tarihi": "09/2024",
            "sorumluluklar": [
                "Verified electrical drawings for standards compliance; conducted inspection/testing of panels and documented deviations",
                "Used Python to structure and visualize inspection data for performance tracking; produced detailed QA documentation"
            ]
        },
        {
            "pozisyon": "Field Engineer",
            "sirket": "AGEST Marine Electrical Technologies",
            "lokasyon": "Antalya, Türkiye",
            "baslangic_tarihi": "06/2021",
            "bitis_tarihi": "03/2024",
            "sorumluluklar": [
                "Led installation teams of 6 to 25 people, ensuring smooth operations and on-time delivery of field projects",
                "Used Python to monitor task progress, detect delays, and support execution decisions",
                "Analyzed material consumption to guide purchasing and improve maintenance planning",
                "Led and participated in installation and production of 18 vessels, including fully electric waterbuses, patrol boats, speedboats, and a 37m superyacht"
            ]
        },
        {
            "pozisyon": "Intern",
            "sirket": "Thyssenkrupp",
            "lokasyon": "Antalya, Türkiye",
            "baslangic_tarihi": "07/2019",
            "bitis_tarihi": "08/2019"
        },
        {
            "pozisyon": "Intern",
            "sirket": "Akdeniz Elektrik Dağıtım A.Ş.",
            "lokasyon": "Antalya, Türkiye",
            "baslangic_tarihi": "07/2017",
            "bitis_tarihi": "08/2017"
        }
    ],
    "egitim": [
        {
            "program": "Data Scientist Bootcamp",
            "kurum": "MIUUL",
            "baslangic_tarihi": "11/2023",
            "bitis_tarihi": "04/2024"
        },
        {
            "program": "B.Sc. Electrical & Electronics Engineering",
            "kurum": "KARADENIZ TECHNICAL UNIVERSITY",
            "lokasyon": "Trabzon, Türkiye",
            "baslangic_tarihi": "2014",
            "bitis_tarihi": "2020"
        }
    ],
    "projeler": [
        {
            "ad": "Telco Customer Churn Prediction",
            "tur": "Classification",
            "teknolojiler": ["Python", "scikit-learn"],
            "aciklama": "Built an end-to-end churn prediction pipeline (EDA, preprocessing, feature engineering, modeling) and evaluated performance with classification metrics (ROC-AUC/F1). Identified key churn drivers and produced customer-level churn risk scores to support retention targeting."
        },
        {
            "ad": "FLO CLTV Prediction",
            "tur": "Customer Value Modeling",
            "teknolojiler": ["Python"],
            "aciklama": "Developed a CLTV prediction workflow to estimate customer lifetime value and enable prioritization for retention/upsell strategies. Delivered customer-level value outputs and actionable insights for marketing decision support."
        },
        {
            "ad": "FLO RFM Customer Segmentation",
            "tur": "Customer Analytics",
            "teknolojiler": ["Python"],
            "aciklama": "Implemented RFM-based segmentation to classify customers by recency, frequency, and monetary value; generated segment-based targeting recommendations."
        },
        {
            "ad": "A/B Testing: Bidding Methods Conversion Comparison",
            "tur": "A/B Testing & Statistics",
            "teknolojiler": ["Python"],
            "aciklama": "Designed and analyzed an A/B test to compare bidding methods on conversion; performed hypothesis testing and reported impact with business-ready conclusions."
        },
        {
            "ad": "Armut / Online Retail Recommendation System",
            "tur": "Association Rules",
            "teknolojiler": ["Python"],
            "aciklama": "Built an association-rule-based recommender system (Apriori) from transaction/service baskets and generated top-N recommendations."
        },
        {
            "ad": "Gezinomi Rule-based Segmentation",
            "tur": "Segmentation & Revenue Estimation",
            "teknolojiler": ["Python"]
        },
        {
            "ad": "Amazon Rating Products and Review Sorting",
            "tur": "Analysis",
            "teknolojiler": ["Python"]
        },
        {
            "ad": "Diabetes Prediction Model",
            "tur": "Classification",
            "teknolojiler": ["Python"]
        }
    ],
    "sosyal_medya_profilleri": {
        "linkedin": "linkedin.com/in/furganince",
        "github": "github.com/furganince",
        "medium": "medium.com/@furganince",
        "email": "furganince@outlook.com"
    },
    "sertifikalar": [
        "Turkcell Sınırsız Yetenek New Graduate Program"
    ],
    "diller": [
        {
            "dil": "Türkçe",
            "seviye": "Native proficiency"
        },
        {
            "dil": "English",
            "seviye": "Professional working proficiency"
        }
    ]
}

if __name__ == "__main__":
    with open('cv_data.json', 'w', encoding='utf-8') as f:
        json.dump(cv_data, f, ensure_ascii=False, indent=2)
    print("✓ CV verileri JSON formatında kaydedildi: cv_data.json")
    print(json.dumps(cv_data, ensure_ascii=False, indent=2))
