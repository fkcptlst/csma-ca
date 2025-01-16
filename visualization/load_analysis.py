import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from data_loader import load_all_results, parse_filename

def analyze_network_load():
    """Analyze network behavior under different loads"""
    results = load_all_results()
    
    # Calculate load-related metrics
    load_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        
        # Calculate offered load and throughput
        offered_load = params['station_count'] * params['frame_rate'] * df['data_rate'].iloc[0]
        actual_throughput = df['bps'].mean()
        
        load_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'offered_load': offered_load,
            'throughput': actual_throughput,
            'collision_rate': df['collision_rate'].mean() * 100,
            'efficiency': (df['processed'] / df['processed_ideal']).mean() * 100
        })
    
    load_df = pd.DataFrame(load_data)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    
    # Plot 1: Throughput vs Offered Load
    sns.scatterplot(data=load_df, x='offered_load', y='throughput',
                    hue='station_count', ax=axes[0,0])
    axes[0,0].set_title('Throughput vs Offered Load')
    axes[0,0].set_xlabel('Offered Load (bps)')
    axes[0,0].set_ylabel('Actual Throughput (bps)')
    
    # Plot 2: Collision Rate vs Load
    sns.scatterplot(data=load_df, x='offered_load', y='collision_rate',
                    hue='station_count', ax=axes[0,1])
    axes[0,1].set_title('Collision Rate vs Load')
    axes[0,1].set_xlabel('Offered Load (bps)')
    axes[0,1].set_ylabel('Collision Rate (%)')
    
    # Plot 3: Efficiency vs Station Count
    sns.boxplot(data=load_df, x='station_count', y='efficiency',
                ax=axes[1,0])
    axes[1,0].set_title('Efficiency vs Network Size')
    axes[1,0].set_ylabel('Processing Efficiency (%)')
    
    # Plot 4: Load Distribution
    sns.histplot(data=load_df, x='offered_load', hue='station_count',
                 multiple="stack", ax=axes[1,1])
    axes[1,1].set_title('Distribution of Offered Loads')
    axes[1,1].set_xlabel('Offered Load (bps)')
    
    plt.tight_layout()
    plt.savefig('results/plots/load_analysis.png')
    plt.close()

if __name__ == "__main__":
    analyze_network_load() 