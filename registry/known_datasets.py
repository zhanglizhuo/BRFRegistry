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
    name="OULAD",
    n=32593,
    n_features=44,
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
    name="Student Dropout",
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
    name="UCI Student",
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
    name="Higher Ed",
    n=145,
    n_features=31,
    target_type="continuous (0-7)",
    n_groups=9,
    source_url="https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation",
    dataset_root="datasets/StudentExam",
    reference="Yilmaz & Sekeroglu (2020); UCI ID 856",
    license_info="CC BY 4.0",
    notes="UCI ID 856. higher_ed_856.csv. Small N.",
)

register_dataset(
    key="mm_tba",
    name="MM-TBA",
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
    n=4217,
    n_features=5,
    target_type="continuous (overall accuracy)",
    n_groups=153,
    source_url="http://base.ustc.edu.cn/data/ASSISTment/2009_skill_builder_data_corrected.zip",
    dataset_root="",
    reference="Feng, Heffernan & Koedinger (2009)",
    license_info="TBD (public research data)",
    notes="Skill builder corrected. Student-level aggregates of 401K transactions. Teacher as group.",
)

register_dataset(
    key="mathe",
    name="MathE",
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
    name="Colleges AAUP",
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
    name="Colleges US News",
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
