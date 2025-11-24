import os
import base64
import io
import pandas as pd
from loguru import logger

COLUMN_NAMES = [
    "timestamp", "level", "userid", "sessionid", "contextid", 
    "requestid", "uniqueid", "error", "message", "description"
]

def parse_csv(content):
    try:
        return pd.read_csv(
            io.StringIO(content), 
            sep=';',
            quotechar='"',
            engine='python', 
            names=COLUMN_NAMES, 
            header=None
        )
    except Exception as e:
        logger.error(f"Błąd parsowania CSV: {e}")
        return pd.DataFrame()

def parse_xlsx(content_base64):
    try:
        decoded = base64.b64decode(content_base64)
        return pd.read_excel(
            io.BytesIO(decoded), 
            names=COLUMN_NAMES, 
            header=None
        )
    except Exception as e:
        logger.error(f"Błąd parsowania XLSX: {e}")
        return pd.DataFrame()

def parse_txt(content):
    data = []
    lines = content.splitlines()

    for line in lines:
        if not line.strip():
            continue

        raw_parts = line.split('\t')
        parts = [p for p in raw_parts if p.strip()]

        raw_level = parts[0]
        level = raw_level
        if ":" in raw_level:
            level = raw_level.split(":")[-1].strip()

        ts = parts[1] if len(parts) > 1 else None
        if ts and ts.count(':') == 3:
            ts = ts[::-1].replace(':', '.', 1)[::-1]

        row = {
            "timestamp": ts,
            "level": level,
            "userid": parts[2] if len(parts) > 2 else None,
            "sessionid": parts[3] if len(parts) > 3 else None,
            "contextid": parts[4] if len(parts) > 4 else None,
            "requestid": parts[5] if len(parts) > 5 else None,
            "uniqueid": parts[6] if len(parts) > 6 else None,
            "error": parts[7] if len(parts) > 7 else None,
            "message": parts[8] if len(parts) > 8 else None,
            "description": parts[9] if len(parts) > 9 else None,
        }
        data.append(row)

    return pd.DataFrame(data, columns=COLUMN_NAMES)

def merge_files(files):
    all_dataframes = []
    
    for file in files or []:
        filename = file.get("name")
        content = file.get("content")
        
        if not filename or content is None:
            continue

        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        df = pd.DataFrame()

        if ext == ".csv":
            df = parse_csv(content)
        elif ext == ".xlsx":
            df = parse_xlsx(content)
        elif ext == ".txt":
            df = parse_txt(content)
        else:
            logger.warning(f"Nieobsługiwany format: {ext}")
            continue

        if not df.empty:
            df["source_file"] = filename
            all_dataframes.append(df)

    if not all_dataframes:
        return {"name": "empty.csv", "content": ""}

    merged_df = pd.concat(all_dataframes, ignore_index=True)

    merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"], errors='coerce')

    merged_df = merged_df.sort_values(by="timestamp", ascending=True, na_position='last')

    output_csv = merged_df.to_csv(index=False, sep=";")
    
    return {
        "name": "merged_data.csv",
        "content": output_csv
    }