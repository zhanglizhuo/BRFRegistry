REGISTRY = {}


def register_dataset(
    key: str,
    name: str,
    n: int,
    n_features: int,
    target_type: str,
    n_groups: int,
    source_url: str,
    dataset_root: str,
    reference: str,
    license_info: str,
    notes: str = "",
):
    REGISTRY[key] = dict(
        key=key,
        name=name,
        n=n,
        n_features=n_features,
        target_type=target_type,
        n_groups=n_groups,
        source_url=source_url,
        dataset_root=dataset_root,
        reference=reference,
        license=license_info,
        notes=notes,
        brf_result=None,
    )


register_dataset(
    key="oulad",
    name="Open University Learning Analytics Dataset",
    n=32593,
    n_features=52,
    target_type="binary (pass/fail)",
    n_groups=22,
    source_url="https://analyse.kmi.open.ac.uk/open_dataset",
    dataset_root="datasets/OULAD",
    reference="Kuzilek et al. (2017)",
    license_info="CC BY-SA 4.0",
    notes="Open University Learning Analytics Dataset. Binarized pass-or-distinction vs fail-or-withdrawn.",
)

register_dataset(
    key="student_dropout",
    name="Student Dropout and Academic Success",
    n=3630,
    n_features=36,
    target_type="binary (Graduate/Dropout)",
    n_groups=17,
    source_url="https://archive.ics.uci.edu/dataset/697/student+dropout+and+academic+success",
    dataset_root="datasets/StudentDropout",
    reference="Realinho et al. (2022); UCI ID 697",
    license_info="CC BY 4.0",
    notes="Excludes 'Enrolled' students.",
)

register_dataset(
    key="xapi_edu",
    name="xAPI-Edu-Data",
    n=480,
    n_features=72,
    target_type="ordinal 3-class (L/M/H)",
    n_groups=12,
    source_url="https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data",
    dataset_root="datasets/xAPI-Edu",
    reference="Amrieh et al. (2016)",
    license_info="CC BY-SA 4.0 (Kaggle)",
    notes="Kalboard 360. Features one-hot encoded.",
)

register_dataset(
    key="entrance_exam",
    name="Entrance Exam",
    n=666,
    n_features=49,
    target_type="ordinal 4-class (0-3)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/582/student+academic+performance",
    dataset_root="datasets/StudentExam",
    reference="Bora & Dey (2021); UCI ID 582",
    license_info="CC BY 4.0",
    notes="UCI ID 582. student_entrance_582.csv.",
)

register_dataset(
    key="uci_student",
    name="UCI Student Performance",
    n=649,
    n_features=56,
    target_type="continuous (0-20)",
    n_groups=2,
    source_url="https://archive.ics.uci.edu/dataset/320/student+performance",
    dataset_root="datasets/UCI",
    reference="Cortez & Silva (2008)",
    license_info="CC BY 4.0",
    notes="Portuguese-language subset. G1 and G2 excluded.",
)

register_dataset(
    key="higher_ed",
    name="Higher Education Students Performance",
    n=145,
    n_features=30,
    target_type="continuous (0-7)",
    n_groups=9,
    source_url="https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation",
    dataset_root="datasets/StudentExam",
    reference="Yilmaz & Sekeroglu (2020); UCI ID 856",
    license_info="CC BY 4.0",
    notes="UCI ID 856. 30 item columns, GRADE as target.",
)

register_dataset(
    key="mm_tba",
    name="MM-TBA Teaching Behavior Analysis",
    n=186,
    n_features=13,
    target_type="continuous (GPT-4 rubric mean)",
    n_groups=0,
    source_url="https://github.com/broadsense/MM-TBA",
    dataset_root="datasets/MM-TBA",
    reference="Huang et al. (2025)",
    license_info="TBD",
    notes="186 lecture segments. No grouping metadata.",
)

register_dataset(
    key="tae",
    name="Teaching Assistant Evaluation",
    n=151,
    n_features=4,
    target_type="ordinal 3-class (Low/Medium/High)",
    n_groups=25,
    source_url="https://archive.ics.uci.edu/dataset/100/teaching+assistant+evaluation",
    dataset_root="",
    reference="Loh (1997); UCI ID 100",
    license_info="CC BY 4.0",
    notes="TA performance from U Wisconsin-Madison Stats Dept. Instructor as group.",
)

register_dataset(
    key="turkiye",
    name="Turkiye Student Evaluation",
    n=5820,
    n_features=28,
    target_type="ordinal 5-class (difficulty 1-5)",
    n_groups=13,
    source_url="https://archive.ics.uci.edu/dataset/262/turkiye+student+evaluation",
    dataset_root="",
    reference="Gazi University; UCI ID 262",
    license_info="CC BY 4.0",
    notes="Student course evaluations from Gazi University, Turkey. Course as group.",
)

register_dataset(
    key="assistments",
    name="ASSISTments 2009-2010",
    n=3729,
    n_features=5,
    target_type="continuous (overall accuracy)",
    n_groups=124,
    source_url="http://base.ustc.edu.cn/data/ASSISTment/2009_skill_builder_data_corrected.zip",
    dataset_root="",
    reference="Feng, Heffernan & Koedinger (2009)",
    license_info="TBD (public research data)",
    notes="Skill builder corrected. Student-level aggregates of 401K transactions. Teacher as group.",
)

register_dataset(
    key="mathe",
    name="MathE Mathematics Learning",
    n=833,
    n_features=26,
    target_type="continuous (question difficulty)",
    n_groups=14,
    source_url="https://archive.ics.uci.edu/dataset/1031/dataset+for+assessing+mathematics+learning+in+higher+education",
    dataset_root="",
    reference="Azevedo, Pacheco, Fernandes & Pereira (2024); UCI ID 1031",
    license_info="CC BY 4.0",
    notes="Question-level aggregation of 9546 student answers. Topic as group.",
)

register_dataset(
    key="colleges_aaup",
    name="AAUP College Faculty Salary",
    n=1161,
    n_features=9,
    target_type="continuous (avg faculty salary)",
    n_groups=52,
    source_url="https://www.openml.org/search?type=data&id=488",
    dataset_root="",
    reference="AAUP Faculty Salary Survey (OpenML ID 488)",
    license_info="Public Domain (OpenML)",
    notes="1161 US colleges, 52 state groups. Institutional-level. Target: average salary all ranks.",
)

register_dataset(
    key="colleges_usnews",
    name="Colleges US News Rankings",
    n=1204,
    n_features=31,
    target_type="continuous (graduation rate)",
    n_groups=51,
    source_url="https://www.openml.org/search?type=data&id=538",
    dataset_root="",
    reference="US News College Rankings (OpenML ID 538)",
    license_info="Public Domain (OpenML)",
    notes="1204 US colleges, 51 state groups. Target: graduation rate.",
)

register_dataset(
    key="college_scorecard",
    name="US College Scorecard",
    n=2220,
    n_features=30,
    target_type="continuous (admission rate)",
    n_groups=55,
    source_url="https://www.openml.org/search?type=data&id=42121",
    dataset_root="",
    reference="US Dept of Education; OpenML ID 42121",
    license_info="Public Domain (OpenML)",
    notes="7804 colleges, filtered to 2220 with admission rate. Target: admission rate.",
)

register_dataset(
    key="oli",
    name="OLI Engineering Statics 2011",
    n=194947,
    n_features=2,
    target_type="binary (first attempt correctness)",
    n_groups=19,
    source_url="http://base.ustc.edu.cn/data/OLI_data.zip",
    dataset_root="",
    reference="CMU OLI; PSLC DataShop",
    license_info="Public research data (PSLC DataShop)",
    notes="194K step-level observations. Target: first attempt correct. Module as group.",
)

register_dataset(
    key="student_depression",
    name="Student Depression Survey",
    n=27875,
    n_features=21,
    target_type="binary (depression yes/no)",
    n_groups=30,
    source_url="https://www.openml.org/search?type=data&id=46753",
    dataset_root="",
    reference="Student Depression Dataset; OpenML ID 46753",
    license_info="Public Domain (OpenML)",
    notes="27.9K students. City as group (30 Indian cities). Run as regression.",
)

register_dataset(
    key="uci_student_math",
    name="UCI Student Performance (Math)",
    n=395,
    n_features=56,
    target_type="continuous (G3 grade)",
    n_groups=2,
    source_url="https://archive.ics.uci.edu/dataset/320/student+performance",
    dataset_root="",
    reference="Cortez & Silva (2008); UCI ID 320 (Math)",
    license_info="CC BY 4.0",
    notes="Portuguese Math subset (student-mat.csv). School as group.",
)

register_dataset(
    key="students_exam_scores",
    name="Students Exam Scores (Kaggle)",
    n=30641,
    n_features=17,
    target_type="continuous (math score)",
    n_groups=5,
    source_url="https://www.kaggle.com/datasets/desalegngeb/students-exam-scores",
    dataset_root="",
    reference="Kaggle: Students Exam Scores",
    license_info="CC0 (Kaggle)",
    notes="30.6K US high school students. Ethnic group (5) as group.",
)

register_dataset(
    key="law_school",
    name="Law School Admission",
    n=20800,
    n_features=7,
    target_type="binary (bar exam pass)",
    n_groups=6,
    source_url="https://www.openml.org/search?type=data&id=43889",
    dataset_root="",
    reference="LSAC; OpenML ID 43889",
    license_info="Public Domain (OpenML)",
    notes="20.8K law school applicants. Cluster (6) as group.",
)

register_dataset(
    key="pisa2015",
    name="PISA 2015 Science",
    n=519334,
    n_features=2,
    target_type="continuous (science score)",
    n_groups=73,
    source_url="http://base.ustc.edu.cn/data/pisa2015_science.zip",
    dataset_root="",
    reference="OECD PISA 2015",
    license_info="OECD Public Use",
    notes="519K students across 73 countries. Country as group.",
)

register_dataset(
    key="abalone",
    name="Abalone Age (Sex groups)",
    n=4177,
    n_features=7,
    target_type="continuous (age via rings)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/1/abalone",
    dataset_root="",
    reference="Nash et al. (1995); UCI ID 1",
    license_info="CC BY 4.0",
    notes="Sex as group (M/F/I).",
)

register_dataset(
    key="airfoil",
    name="Airfoil Noise (Freq)",
    n=1503,
    n_features=4,
    target_type="continuous (sound pressure)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/291/airfoil+self+noise",
    dataset_root="",
    reference="Brooks et al. (1989); UCI ID 291",
    license_info="CC BY 4.0",
    notes="Frequency bins as groups.",
)

register_dataset(
    key="auto_mpg",
    name="Auto MPG (Origin groups)",
    n=392,
    n_features=6,
    target_type="continuous (mpg)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/9/auto+mpg",
    dataset_root="",
    reference="Quinlan (1993); UCI ID 9",
    license_info="CC BY 4.0",
    notes="Origin (US/Europe/Japan) as group.",
)

register_dataset(
    key="bike_sharing",
    name="Bike Sharing (Season)",
    n=731,
    n_features=10,
    target_type="continuous (bike count)",
    n_groups=4,
    source_url="https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset",
    dataset_root="",
    reference="Fanaee-T & Gama (2013); UCI ID 275",
    license_info="CC BY 4.0",
    notes="Season as group. Day-level aggregation.",
)

register_dataset(
    key="ccpp",
    name="Combined Cycle Power (Temp)",
    n=9568,
    n_features=3,
    target_type="continuous (net hourly energy)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant",
    dataset_root="",
    reference="Tufekci (2014); UCI ID 294",
    license_info="CC BY 4.0",
    notes="Temperature bins as groups.",
)

register_dataset(
    key="concrete",
    name="Concrete Strength (Age)",
    n=1030,
    n_features=7,
    target_type="continuous (compressive strength)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength",
    dataset_root="",
    reference="Yeh (1998); UCI ID 165",
    license_info="CC BY 4.0",
    notes="Age bins as groups.",
)

register_dataset(
    key="energy_building",
    name="Energy Building (Orientation)",
    n=768,
    n_features=7,
    target_type="continuous (heating load)",
    n_groups=4,
    source_url="https://archive.ics.uci.edu/dataset/242/energy+efficiency",
    dataset_root="",
    reference="Tsanas & Xifara (2012); UCI ID 242",
    license_info="CC BY 4.0",
    notes="Orientation as group.",
)

register_dataset(
    key="kaggle_students_performance",
    name="Kaggle Students Performance in Exams",
    n=1000,
    n_features=17,
    target_type="continuous (math score)",
    n_groups=5,
    source_url="https://www.kaggle.com/datasets/spscientist/students-performance-in-exams",
    dataset_root="",
    reference="Kaggle (spscientist); originally from NCES",
    license_info="CC0: Public Domain (Kaggle)",
    notes="Race/ethnicity as group (5 categories A-E).",
)

register_dataset(
    key="kdd_cup_2010",
    name="KDD Cup 2010 (Algebra I 2005-2006)",
    n=574,
    n_features=5,
    target_type="continuous (mean correct first attempt)",
    n_groups=22,
    source_url="http://base.ustc.edu.cn/data/KDD_Cup_2010/algebra_2005_2006.zip",
    dataset_root="",
    reference="Stamper, Niculescu-Mizil, Ritter, Gordon & Koedinger (2010)",
    license_info="Public research data (PSLC DataShop)",
    notes="Student-level aggregation of 809K step logs from Algebra I 2005-2006. Curriculum unit as group.",
)

register_dataset(
    key="nursery",
    name="UCI Nursery School Applications",
    n=12960,
    n_features=24,
    target_type="continuous (rank ordinal 1-5)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/76/nursery",
    dataset_root="",
    reference="Olave, Rajkovic & Bohanec (1989); UCI ID 76",
    license_info="CC BY 4.0",
    notes="Parents occupation as group (3 levels).",
)

register_dataset(
    key="real_estate",
    name="Real Estate Valuation (Stores)",
    n=414,
    n_features=4,
    target_type="continuous (unit price)",
    n_groups=3,
    source_url="https://archive.ics.uci.edu/dataset/477/real+estate+valuation",
    dataset_root="",
    reference="Yeh & Hsu (2018); UCI ID 477",
    license_info="CC BY 4.0",
    notes="Convenience stores count binned as group.",
)

register_dataset(
    key="seoul_bike",
    name="Seoul Bike Sharing (Season)",
    n=8760,
    n_features=9,
    target_type="continuous (bike rental count)",
    n_groups=4,
    source_url="https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand",
    dataset_root="",
    reference="Sathishkumar et al. (2020); UCI ID 560",
    license_info="CC BY 4.0",
    notes="Season as group.",
)

register_dataset(
    key="student_absences",
    name="UCI Student Absences (Kaggle)",
    n=395,
    n_features=55,
    target_type="continuous (absence count)",
    n_groups=2,
    source_url="https://www.kaggle.com/datasets/uciml/student-alcohol-consumption",
    dataset_root="",
    reference="Cortez & Silva (2008); UCI ID 320 (Kaggle mirror)",
    license_info="CC BY 4.0",
    notes="School (GP/MS) as group. Renamed from student_alcohol.",
)

register_dataset(
    key="student_health",
    name="UCI Student Health (Por, Mjob)",
    n=649,
    n_features=53,
    target_type="continuous (health status)",
    n_groups=5,
    source_url="https://www.kaggle.com/datasets/uciml/student-alcohol-consumption",
    dataset_root="",
    reference="Cortez & Silva (2008); UCI ID 320 (Kaggle mirror, health target)",
    license_info="CC BY 4.0",
    notes="Mother's job as group (5 categories).",
)

register_dataset(
    key="wine_quality",
    name="Wine Quality (Red+White)",
    n=6497,
    n_features=11,
    target_type="continuous (quality score)",
    n_groups=2,
    source_url="https://archive.ics.uci.edu/dataset/186/wine+quality",
    dataset_root="",
    reference="Cortez et al. (2009); UCI ID 186",
    license_info="CC BY 4.0",
    notes="Wine type (red/white) as group.",
)
