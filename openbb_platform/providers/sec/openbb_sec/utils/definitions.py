"""SEC Definitions and Models."""

from typing import Dict, Literal

QUARTERS = Literal[1, 2, 3, 4]

SEC_HEADERS: Dict[str, str] = {
    "User-Agent": "my real company name definitelynot@fakecompany.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.sec.gov",
}

# Some endpoints don't like the Host header.

HEADERS: Dict[str, str] = {
    "User-Agent": "my real company name definitelynot@fakecompany.com",
    "Accept-Encoding": "gzip, deflate",
}


FORM_TYPES = Literal[
    "1",
    "1-A",
    "1-A_POS",
    "1-A-W",
    "1-E",
    "1-E_AD",
    "1-K",
    "1-SA",
    "1-U",
    "1-Z",
    "1-Z-W",
    "10-12B",
    "10-12G",
    "10-D",
    "10-K",
    "10-KT",
    "10-Q",
    "10-QT",
    "11-K",
    "11-KT",
    "13F-HR",
    "13F-NT",
    "13FCONP",
    "144",
    "15-12B",
    "15-12G",
    "15-15D",
    "15F-12B",
    "15F-12G",
    "15F-15D",
    "18-12B",
    "18-K",
    "19B-4E",
    "2-A",
    "2-AF",
    "2-E",
    "20-F",
    "20FR12B",
    "20FR12G",
    "24F-2NT",
    "25",
    "25-NSE",
    "253G1",
    "253G2",
    "253G3",
    "253G4",
    "3",
    "305B2",
    "34-12H",
    "4",
    "40-17F1",
    "40-17F2",
    "40-17G",
    "40-17GCS",
    "40-202A",
    "40-203A",
    "40-206A",
    "40-24B2",
    "40-33",
    "40-6B",
    "40-8B25",
    "40-8F-2",
    "40-APP",
    "40-F",
    "40-OIP",
    "40FR12B",
    "40FR12G",
    "424A",
    "424B1",
    "424B2",
    "424B3",
    "424B4",
    "424B5",
    "424B7",
    "424B8",
    "424H",
    "425",
    "485APOS",
    "485BPOS",
    "485BXT",
    "486APOS",
    "486BPOS",
    "486BXT",
    "487",
    "497",
    "497AD",
    "497H2",
    "497J",
    "497K",
    "497VPI",
    "497VPU",
    "5",
    "6-K",
    "6B_NTC",
    "6B_ORDR",
    "8-A12B",
    "8-A12G",
    "8-K",
    "8-K12B",
    "8-K12G3",
    "8-K15D5",
    "8-M",
    "8F-2_NTC",
    "8F-2_ORDR",
    "9-M",
    "ABS-15G",
    "ABS-EE",
    "ADN-MTL",
    "ADV-E",
    "ADV-H-C",
    "ADV-H-T",
    "ADV-NR",
    "ANNLRPT",
    "APP_NTC",
    "APP_ORDR",
    "APP_WD",
    "APP_WDG",
    "ARS",
    "ATS-N",
    "ATS-N-C",
    "ATS-N/UA",
    "AW",
    "AW_WD",
    "C",
    "C-AR",
    "C-AR-W",
    "C-TR",
    "C-TR-W",
    "C-U",
    "C-U-W",
    "C-W",
    "CB",
    "CERT",
    "CERTARCA",
    "CERTBATS",
    "CERTCBO",
    "CERTNAS",
    "CERTNYS",
    "CERTPAC",
    "CFPORTAL",
    "CFPORTAL-W",
    "CORRESP",
    "CT_ORDER",
    "D",
    "DEF_14A",
    "DEF_14C",
    "DEFA14A",
    "DEFA14C",
    "DEFC14A",
    "DEFC14C",
    "DEFM14A",
    "DEFM14C",
    "DEFN14A",
    "DEFR14A",
    "DEFR14C",
    "DEL_AM",
    "DFAN14A",
    "DFRN14A",
    "DOS",
    "DOSLTR",
    "DRS",
    "DRSLTR",
    "DSTRBRPT",
    "EFFECT",
    "F-1",
    "F-10",
    "F-10EF",
    "F-10POS",
    "F-1MEF",
    "F-3",
    "F-3ASR",
    "F-3D",
    "F-3DPOS",
    "F-3MEF",
    "F-4",
    "F-4_POS",
    "F-4MEF",
    "F-6",
    "F-6_POS",
    "F-6EF",
    "F-7",
    "F-7_POS",
    "F-8",
    "F-8_POS",
    "F-80",
    "F-80POS",
    "F-9",
    "F-9_POS",
    "F-N",
    "F-X",
    "FOCUSN",
    "FWP",
    "G-405",
    "G-405N",
    "G-FIN",
    "G-FINW",
    "IRANNOTICE",
    "MA",
    "MA-A",
    "MA-I",
    "MA-W",
    "MSD",
    "MSDCO",
    "MSDW",
    "N-1",
    "N-14",
    "N-14_8C",
    "N-14MEF",
    "N-18F1",
    "N-1A",
    "N-2",
    "N-2_POSASR",
    "N-23C-2",
    "N-23C3A",
    "N-23C3B",
    "N-23C3C",
    "N-2ASR",
    "N-2MEF",
    "N-30B-2",
    "N-30D",
    "N-4",
    "N-5",
    "N-54A",
    "N-54C",
    "N-6",
    "N-6F",
    "N-8A",
    "N-8B-2",
    "N-8F",
    "N-8F_NTC",
    "N-8F_ORDR",
    "N-CEN",
    "N-CR",
    "N-CSR",
    "N-CSRS",
    "N-MFP",
    "N-MFP1",
    "N-MFP2",
    "N-PX",
    "N-Q",
    "N-VP",
    "N-VPFS",
    "NO_ACT",
    "NPORT-EX",
    "NPORT-NP",
    "NPORT-P",
    "NRSRO-CE",
    "NRSRO-UPD",
    "NSAR-A",
    "NSAR-AT",
    "NSAR-B",
    "NSAR-BT",
    "NSAR-U",
    "NT_10-D",
    "NT_10-K",
    "NT_10-Q",
    "NT_11-K",
    "NT_20-F",
    "NT_N-CEN",
    "NT_N-MFP",
    "NT_N-MFP1",
    "NT_N-MFP2",
    "NT_NPORT-EX",
    "NT_NPORT-P",
    "NT-NCEN",
    "NT-NCSR",
    "NT-NSAR",
    "NTFNCEN",
    "NTFNCSR",
    "NTFNSAR",
    "NTN_10D",
    "NTN_10K",
    "NTN_10Q",
    "NTN_20F",
    "OIP_NTC",
    "OIP_ORDR",
    "POS_8C",
    "POS_AM",
    "POS_AMI",
    "POS_EX",
    "POS462B",
    "POS462C",
    "POSASR",
    "PRE_14A",
    "PRE_14C",
    "PREC14A",
    "PREC14C",
    "PREM14A",
    "PREM14C",
    "PREN14A",
    "PRER14A",
    "PRER14C",
    "PRRN14A",
    "PX14A6G",
    "PX14A6N",
    "QRTLYRPT",
    "QUALIF",
    "REG-NR",
    "REVOKED",
    "RW",
    "RW_WD",
    "S-1",
    "S-11",
    "S-11MEF",
    "S-1MEF",
    "S-20",
    "S-3",
    "S-3ASR",
    "S-3D",
    "S-3DPOS",
    "S-3MEF",
    "S-4",
    "S-4_POS",
    "S-4EF",
    "S-4MEF",
    "S-6",
    "S-8",
    "S-8_POS",
    "S-B",
    "S-BMEF",
    "SBSE",
    "SBSE-A",
    "SBSE-BD",
    "SBSE-C",
    "SBSE-W",
    "SC_13D",
    "SC_13E1",
    "SC_13E3",
    "SC_13G",
    "SC_14D9",
    "SC_14F1",
    "SC_14N",
    "SC_TO-C",
    "SC_TO-I",
    "SC_TO-T",
    "SC13E4F",
    "SC14D1F",
    "SC14D9C",
    "SC14D9F",
    "SD",
    "SDR",
    "SE",
    "SEC_ACTION",
    "SEC_STAFF_ACTION",
    "SEC_STAFF_LETTER",
    "SF-1",
    "SF-3",
    "SL",
    "SP_15D2",
    "STOP_ORDER",
    "SUPPL",
    "T-3",
    "TA-1",
    "TA-2",
    "TA-W",
    "TACO",
    "TH",
    "TTW",
    "UNDER",
    "UPLOAD",
    "WDL-REQ",
    "X-17A-5",
]


TAXONOMIES = Literal["us-gaap", "dei", "ifrs-full", "srt"]