import os
import pandas as pd
from typing import List, Dict

def load_all_results(csv_dir: str = "results/csv") -> Dict[str, pd.DataFrame]:
    """Load all CSV files from results directory"""
    results = {}
    for file in os.listdir(csv_dir):
        if file.endswith('.csv'):
            path = os.path.join(csv_dir, file)
            key = file.replace('.csv', '')
            results[key] = pd.read_csv(path)
    return results

def parse_filename(filename: str) -> Dict:
    """Parse filename into parameters"""
    parts = filename.split('_')
    return {
        'station_count': int(parts[0]),
        'frame_rate': int(parts[2]),
        'backoff_min': int(parts[4])
    } 