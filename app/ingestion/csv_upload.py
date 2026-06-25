import pandas as pd
def load_csv(file_path):
        df=pd.read_csv(file_path)
        # 1. Drop entirely empty rows and columns
        df.dropna(how='all', inplace=True)
        # 2. Drop duplicate rows to keep data pristine
        df.drop_duplicates(inplace=True)
        # 3. Clean up edge string spaces across all categorical rows
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
        raw_text = df.to_string()
        return raw_text