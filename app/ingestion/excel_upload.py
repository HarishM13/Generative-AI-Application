import pandas as pd
def load_excel(file_path):
    xls=pd.ExcelFile(file_path)
    out=""
    for s in xls.sheet_names:
        df=pd.read_excel(file_path,sheet_name=s)
         # 1. Drop entirely empty rows and columns
        df.dropna(how='all', inplace=True)
        # 2. Drop duplicate rows to keep data pristine
        df.drop_duplicates(inplace=True)
        # 3. Clean up edge string spaces across all categorical rows
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
        out= df.to_string()
        return out
