import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from data_loader import parse_filename

def load_and_process_results(rts_dir: str, no_rts_dir: str):
    """Load and process results from both directories"""
    
    def load_dir_results(directory, rts_type):
        results = []
        for file in Path(directory).glob('*.csv'):
            try:
                df = pd.read_csv(file)
                params = parse_filename(file.stem)
                
                # Calculate metrics per configuration
                results.append({
                    'station_count': params['station_count'],
                    'frame_rate': params['frame_rate'],
                    'backoff_min': params['backoff_min'],
                    'throughput': df['bps'].mean(),
                    'throughput_std': df['bps'].std(),
                    'collision_rate': df['collision_rate'].mean() * 100,
                    'efficiency': (df['processed'] / df['processed_ideal']).mean() * 100,
                    'wasted_time': df['wasted'].mean(),
                    'total_collisions': df['collisions'].sum(),
                    'frames_sent': df['sent'].sum(),
                    'frames_processed': df['processed'].sum(),
                    'with_rts': rts_type
                })
                print(f"Loaded {file.name} - {rts_type}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
        return pd.DataFrame(results)
    
    print("\nLoading RTS/CTS results...")
    rts_results = load_dir_results(rts_dir, 'RTS/CTS')
    print("\nLoading Basic CSMA/CA results...")
    no_rts_results = load_dir_results(no_rts_dir, 'Basic')
    
    # Verify data loading
    print(f"\nLoaded {len(rts_results)} RTS/CTS configurations")
    print(f"Loaded {len(no_rts_results)} Basic configurations")
    
    combined_df = pd.concat([rts_results, no_rts_results], ignore_index=True)
    
    # Verify combined data
    print("\nData summary:")
    print(combined_df.groupby('with_rts').size())
    
    return combined_df

def analyze_rts_impact():
    """Compare performance between RTS/CTS and non-RTS/CTS scenarios"""
    
    df = load_and_process_results('results/csv-rtscts', 'results/csv-wo-rtscts')
    
    # Verify we have both types of data
    rts_counts = df['with_rts'].value_counts()
    if len(rts_counts) != 2:
        print("Warning: Missing data for one or more RTS configurations!")
        print("Available data:")
        print(rts_counts)
        return
        
    # Figure 1: Core Performance Metrics
    fig1, axes1 = plt.subplots(2, 2, figsize=(15, 15))
    
    # Throughput Comparison
    sns.boxplot(data=df, x='station_count', y='throughput',
                hue='with_rts', ax=axes1[0,0])
    axes1[0,0].set_title('Network Throughput Comparison')
    axes1[0,0].set_ylabel('Throughput (Kbps)')
    
    # Collision Rate Comparison
    sns.boxplot(data=df, x='station_count', y='collision_rate',
                hue='with_rts', ax=axes1[0,1])
    axes1[0,1].set_title('Collision Rate Comparison')
    axes1[0,1].set_ylabel('Collision Rate (%)')
    
    # Success Rate (Processed/Sent)
    df['success_rate'] = (df['frames_processed'] / df['frames_sent']) * 100
    sns.boxplot(data=df, x='station_count', y='success_rate',
                hue='with_rts', ax=axes1[1,0])
    axes1[1,0].set_title('Frame Success Rate')
    axes1[1,0].set_ylabel('Success Rate (%)')
    
    # Efficiency Comparison
    sns.boxplot(data=df, x='station_count', y='efficiency',
                hue='with_rts', ax=axes1[1,1])
    axes1[1,1].set_title('Network Efficiency')
    axes1[1,1].set_ylabel('Efficiency (%)')
    
    plt.tight_layout()
    plt.savefig('results/plots/rts_core_metrics.png')
    plt.close()
    
    # Figure 2: Performance under Different Loads
    fig2, axes2 = plt.subplots(2, 2, figsize=(15, 15))
    
    # High Load vs Low Load Analysis
    df['network_load'] = df['station_count'] * df['frame_rate']
    df['load_category'] = pd.qcut(df['network_load'], q=3, labels=['Low', 'Medium', 'High'])
    
    # Throughput vs Load
    sns.boxplot(data=df, x='load_category', y='throughput',
                hue='with_rts', ax=axes2[0,0])
    axes2[0,0].set_title('Throughput vs Network Load')
    axes2[0,0].set_ylabel('Throughput (Kbps)')
    
    # Collision Rate vs Load
    sns.boxplot(data=df, x='load_category', y='collision_rate',
                hue='with_rts', ax=axes2[0,1])
    axes2[0,1].set_title('Collision Rate vs Network Load')
    axes2[0,1].set_ylabel('Collision Rate (%)')
    
    # Backoff Impact Analysis
    sns.lineplot(data=df, x='backoff_min', y='collision_rate',
                hue='with_rts', style='load_category', ax=axes2[1,0])
    axes2[1,0].set_title('Collision Rate vs Backoff Window')
    axes2[1,0].set_ylabel('Collision Rate (%)')
    
    # Efficiency vs Load
    sns.boxplot(data=df, x='load_category', y='efficiency',
                hue='with_rts', ax=axes2[1,1])
    axes2[1,1].set_title('Efficiency vs Network Load')
    axes2[1,1].set_ylabel('Efficiency (%)')
    
    plt.tight_layout()
    plt.savefig('results/plots/rts_load_analysis.png')
    plt.close()
    
    # Statistical Analysis
    print("\nRTS/CTS Impact Analysis:")
    print("------------------------")
    
    # Performance comparison for different network sizes
    for station_count in df['station_count'].unique():
        mask = df['station_count'] == station_count
        rts_data = df[mask & (df['with_rts'] == 'RTS/CTS')]
        basic_data = df[mask & (df['with_rts'] == 'Basic')]
        
        print(f"\nStation Count: {station_count}")
        print(f"Throughput: RTS/CTS={rts_data['throughput'].mean():.1f} vs Basic={basic_data['throughput'].mean():.1f} Kbps")
        print(f"Collision Rate: RTS/CTS={rts_data['collision_rate'].mean():.1f}% vs Basic={basic_data['collision_rate'].mean():.1f}%")
        print(f"Success Rate: RTS/CTS={rts_data['success_rate'].mean():.1f}% vs Basic={basic_data['success_rate'].mean():.1f}%")
    
    # Save detailed statistics
    stats_df = df.groupby(['with_rts', 'load_category']).agg({
        'throughput': ['mean', 'std'],
        'collision_rate': ['mean', 'std'],
        'efficiency': ['mean', 'std'],
        'success_rate': ['mean', 'std']
    }).round(2)
    
    stats_df.to_csv('results/plots/rts_detailed_statistics.csv')

if __name__ == "__main__":
    analyze_rts_impact() 