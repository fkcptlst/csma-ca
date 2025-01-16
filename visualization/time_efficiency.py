import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from data_loader import load_all_results, parse_filename

def analyze_time_efficiency():
    """Analyze time utilization and efficiency metrics"""
    results = load_all_results()
    
    # Prepare time efficiency data
    efficiency_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        
        # Calculate efficiency metrics
        processing_efficiency = (df['processed'] / df['processed_ideal']).mean() * 100
        wasted_time_ratio = df['wasted'].sum() / df['current'].max() * 100
        
        efficiency_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'backoff_min': params['backoff_min'],
            'processing_efficiency': processing_efficiency,
            'wasted_time_ratio': wasted_time_ratio,
            'avg_wasted_time': df['wasted'].mean()
        })
    
    eff_df = pd.DataFrame(efficiency_data)
    
    # Create visualization grid
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    # Plot 1: Processing Efficiency vs Station Count and Frame Rate
    # Aggregate duplicate combinations by taking the mean
    pivot_data1 = eff_df.groupby(['station_count', 'frame_rate'])['processing_efficiency'].mean().unstack()
    sns.heatmap(pivot_data1, annot=True, fmt='.1f', ax=axes[0], cmap='YlOrRd')
    axes[0].set_title('Processing Efficiency (%) vs Station Count and Frame Rate')
    
    # Plot 2: Wasted Time Analysis
    # Aggregate duplicate combinations by taking the mean
    pivot_data2 = eff_df.groupby(['backoff_min', 'station_count'])['wasted_time_ratio'].mean().unstack()
    sns.heatmap(pivot_data2, annot=True, fmt='.1f', ax=axes[1], cmap='YlOrRd')
    axes[1].set_title('Wasted Time Ratio (%) vs Backoff and Station Count')
    
    plt.tight_layout()
    plt.savefig('results/plots/time_efficiency.png')
    plt.close()

    # Additional analysis: Line plots for better visualization of trends
    fig, axes = plt.subplots(2, 1, figsize=(12, 12))
    
    # Plot 3: Processing Efficiency vs Station Count for different Frame Rates
    for frame_rate in eff_df['frame_rate'].unique():
        mask = eff_df['frame_rate'] == frame_rate
        sns.lineplot(data=eff_df[mask], x='station_count', y='processing_efficiency', 
                    label=f'Frame Rate: {frame_rate}', ax=axes[0], marker='o')
    axes[0].set_title('Processing Efficiency vs Station Count')
    axes[0].set_ylabel('Processing Efficiency (%)')
    axes[0].grid(True)
    
    # Plot 4: Wasted Time vs Backoff for different Station Counts
    for station_count in eff_df['station_count'].unique():
        mask = eff_df['station_count'] == station_count
        sns.lineplot(data=eff_df[mask], x='backoff_min', y='wasted_time_ratio',
                    label=f'Stations: {station_count}', ax=axes[1], marker='o')
    axes[1].set_title('Wasted Time vs Backoff Window')
    axes[1].set_ylabel('Wasted Time Ratio (%)')
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('results/plots/time_efficiency_trends.png')
    plt.close()

if __name__ == "__main__":
    analyze_time_efficiency() 