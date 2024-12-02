# SEC EDGAR Tags Dictionary
sec_tags = {
    # SEC Header Tags
    'header_tags': [
        'SEC-HEADER',
        'ACCEPTANCE-DATETIME',
        'ACCESSION-NUMBER',
        'FILER',
        'COMPANY-DATA',
        'FILING-VALUES',
        'PUBLIC-DOCUMENT-COUNT',
        'FILED-DATE',
        'PERIOD',
        'SROS',
        'SUBMISSION-TYPE',
    ],
    
    # Document Structure Tags
    'document_tags': [
        'DOCUMENT',
        'TYPE',
        'SEQUENCE',
        'FILENAME',
        'DESCRIPTION',
        'TEXT',
    ],
    
    # XBRL Related Tags
    'xbrl_tags': [
        'ix:continuation',
        'ix:denominator',
        'ix:exclude',
        'ix:footnote',
        'ix:fraction',
        'ix:header',
        'ix:hidden',
        'ix:nonFraction',
        'ix:nonNumeric',
        'ix:numerator',
        'ix:references',
        'ix:relationship',
        'ix:resources',
        'ix:tuple',
        'link:schemaRef',
        'xbrli:context',
        'xbrli:measure',
        'xbrli:unit',
    ],
    
    # Common HTML Style Tags
    'style_tags': [
        'FONT',
        'CENTER',
        'B',
        'I',
        'U',
        'SUB',
        'SUP',
        'STRIKE',
        'SMALL',
        'BIG',
    ],
    
    # Table Related Tags
    'table_tags': [
        'TABLE',
        'TR',
        'TD',
        'TH',
        'THEAD',
        'TBODY',
        'TFOOT',
        'CAPTION',
        'COL',
        'COLGROUP',
    ],
    
    # Layout and Structure Tags
    'layout_tags': [
        'DIV',
        'SPAN',
        'P',
        'BR',
        'HR',
        'PRE',
        'BLOCKQUOTE',
        'UL',
        'OL',
        'LI',
        'DL',
        'DT',
        'DD',
    ],
    
    # SEC-Specific Content Tags
    'content_tags': [
        'RISK-FACTORS',
        'BUSINESS',
        'PROPERTIES',
        'LEGAL-PROCEEDINGS',
        'MINE-SAFETY-DISCLOSURES',
        'MARKET',
        'MANAGEMENT-DISCUSSION',
        'FINANCIAL-STATEMENTS',
        'CHANGES-DISAGREEMENTS',
        'CONTROLS-PROCEDURES',
        'OTHER-INFORMATION',
        'DIRECTORS-OFFICERS',
        'EXECUTIVE-COMPENSATION',
        'SECURITY-OWNERSHIP',
        'RELATIONSHIPS-TRANSACTIONS',
        'PRINCIPAL-ACCOUNTANT-FEES',
        'EXHIBITS',
    ],
    
    # Meta Tags
    'meta_tags': [
        'HEAD',
        'META',
        'TITLE',
        'LINK',
        'STYLE',
        'SCRIPT',
    ],
    
    # Special Characters and Entities
    'special_chars': [
        '&nbsp;',
        '&lt;',
        '&gt;',
        '&amp;',
        '&quot;',
        '&apos;',
        '&cent;',
        '&pound;',
        '&euro;',
        '&reg;',
        '&copy;',
        '&trade;',
    ],
    
    # Common Attributes
    'common_attributes': [
        'class',
        'style',
        'align',
        'width',
        'height',
        'bgcolor',
        'colspan',
        'rowspan',
        'contextRef',
        'unitRef',
        'decimals',
        'scale',
        'format',
        'name',
    ]
}

# Common CSS Classes (often need to be cleaned or standardized)
common_css_classes = [
    'company-info',
    'financial-table',
    'section-header',
    'table-header',
    'footnote',
    'bold',
    'italic',
    'underline',
    'center',
    'right',
    'left',
    'indent',
    'smallcaps',
    'redline',
    'strikethrough',
]

# Common table types (useful for identifying specific financial tables)
financial_table_types = [
    'balance-sheet',
    'income-statement',
    'cash-flow',
    'shareholders-equity',
    'ratio-analysis',
    'segment-information',
    'notes-to-financial-statements',
]





patterns_to_remove = [
        r"[A-Za-z0-9+/]{40,}",  # long base64-like sequences
        r"[M]{10,}",            # sequences with repeated characters
        r"end$",                # lines that containing 'end'
        r"begin 644",           # encoding artifacts like 'begin 644'
        r"\b[A-Za-z0-9]{30,}\b", # alphanumeric characters
        r"\*+",                 # symbols like * or ** (one or more * symbols)
    ]

# Statement terms to identify 
statement_terms = [
    "PERIOD-TYPE",
    "FISCAL-YEAR-END",
    "PERIOD-END",
    "EXCHANGE-RATE",
    "CASH",
    "SECURITIES",
    "RECEIVABLES",
    "ALLOWANCES",
    "INVENTORY",
    "CURRENT-ASSETS",
    "PP&E",
    "DEPRECIATION",
    "TOTAL-ASSETS",
    "CURRENT-LIABILITIES",
    "BONDS",
    "PREFERRED-MANDATORY",
    "PREFERRED",
    "COMMON",
    "OTHER-SE",
    "TOTAL-LIABILITY-AND-EQUITY",
    "SALES",
    "TOTAL-REVENUES",
    "CGS",
    "TOTAL-COSTS",
    "OTHER-EXPENSES",
    "LOSS-PROVISION",
    "INTEREST-EXPENSE",
    "INCOME-PRETAX",
    "INCOME-TAX",
    "INCOME-CONTINUING",
    "DISCONTINUED",
    "EXTRAORDINARY",
    "CHANGES",
    "NET-INCOME",
    "EPS-PRIMARY",
    "EPS-DILUTED"
]