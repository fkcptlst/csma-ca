import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from data_loader import load_all_results, parse_filename

def analyze_key_factors():
    """Analyze the impact of the three main varying factors"""
    results = load_all_results()
    
    # Prepare data
    factor_data = []
    for filename, df in results.items():
        params = parse_filename(filename)
        factor_data.append({
            'station_count': params['station_count'],
            'frame_rate': params['frame_rate'],
            'backoff_min': params['backoff_min'],
            'throughput': df['bps'].mean(),
            'collision_rate': df['collision_rate'].mean() * 100,
            'efficiency': (df['processed'] / df['processed_ideal']).mean() * 100,
            'wasted_time': df['wasted'].mean()
        })
    
    df = pd.DataFrame(factor_data)
    
    # Create multiple figures for different aspects
    
    # Figure 1: Station Count Analysis
    fig1, axes1 = plt.subplots(2, 2, figsize=(15, 15))
    
    # Throughput vs Station Count for different frame rates
    sns.boxplot(data=df, x='station_count', y='throughput', 
                hue='frame_rate', ax=axes1[0,0])
    axes1[0,0].set_title('Throughput vs Station Count')
    axes1[0,0].set_ylabel('Throughput (Kbps)')
    
    # Collision Rate vs Station Count for different backoff values
    sns.boxplot(data=df, x='station_count', y='collision_rate',
                hue='backoff_min', ax=axes1[0,1])
    axes1[0,1].set_title('Collision Rate vs Station Count')
    axes1[0,1].set_ylabel('Collision Rate (%)')
    
    # Efficiency heatmap: Station Count vs Frame Rate
    pivot = df.pivot_table(values='efficiency', 
                          index='station_count',
                          columns='frame_rate',
                          aggfunc='mean')
    sns.heatmap(pivot, annot=True, fmt='.1f', ax=axes1[1,0], cmap='YlOrRd')
    axes1[1,0].set_title('Efficiency: Station Count vs Frame Rate')
    
    # Wasted Time vs Station Count
    sns.boxplot(data=df, x='station_count', y='wasted_time', ax=axes1[1,1])
    axes1[1,1].set_title('Wasted Time vs Station Count')
    axes1[1,1].set_ylabel('Average Wasted Time')
    
    plt.tight_layout()
    plt.savefig('results/plots/station_count_analysis.png')
    plt.close()
    
    # Figure 2: Backoff Analysis
    fig2, axes2 = plt.subplots(2, 2, figsize=(15, 15))
    
    # Throughput vs Backoff for different station counts
    sns.boxplot(data=df, x='backoff_min', y='throughput',
                hue='station_count', ax=axes2[0,0])
    axes2[0,0].set_title('Throughput vs Backoff Window')
    axes2[0,0].set_ylabel('Throughput (Kbps)')
    
    # Collision Rate vs Backoff
    sns.boxplot(data=df, x='backoff_min', y='collision_rate', ax=axes2[0,1])
    axes2[0,1].set_title('Collision Rate vs Backoff Window')
    axes2[0,1].set_ylabel('Collision Rate (%)')
    
    # Efficiency heatmap: Backoff vs Frame Rate
    pivot = df.pivot_table(values='efficiency',
                          index='backoff_min',
                          columns='frame_rate',
                          aggfunc='mean')
    sns.heatmap(pivot, annot=True, fmt='.1f', ax=axes2[1,0], cmap='YlOrRd')
    axes2[1,0].set_title('Efficiency: Backoff vs Frame Rate')
    
    # Wasted Time vs Backoff for different station counts
    sns.boxplot(data=df, x='backoff_min', y='wasted_time',
                hue='station_count', ax=axes2[1,1])
    axes2[1,1].set_title('Wasted Time vs Backoff Window')
    axes2[1,1].set_ylabel('Average Wasted Time')
    
    plt.tight_layout()
    plt.savefig('results/plots/backoff_analysis.png')
    plt.close()
    
    # Figure 3: Frame Rate Analysis
    fig3, axes3 = plt.subplots(2, 2, figsize=(15, 15))
    
    # Throughput vs Frame Rate for different station counts
    sns.lineplot(data=df, x='frame_rate', y='throughput',
                 hue='station_count', marker='o', ax=axes3[0,0])
    axes3[0,0].set_title('Throughput vs Frame Rate')
    axes3[0,0].set_ylabel('Throughput (Kbps)')
    
    # Collision Rate vs Frame Rate
    sns.lineplot(data=df, x='frame_rate', y='collision_rate',
                 hue='station_count', marker='o', ax=axes3[0,1])
    axes3[0,1].set_title('Collision Rate vs Frame Rate')
    axes3[0,1].set_ylabel('Collision Rate (%)')
    
    # Efficiency heatmap: Frame Rate vs Backoff
    pivot = df.pivot_table(values='efficiency',
                          index='frame_rate',
                          columns='backoff_min',
                          aggfunc='mean')
    sns.heatmap(pivot, annot=True, fmt='.1f', ax=axes3[1,0], cmap='YlOrRd')
    axes3[1,0].set_title('Efficiency: Frame Rate vs Backoff')
    
    # Network Load vs Frame Rate
    df['network_load'] = df['station_count'] * df['frame_rate']
    sns.scatterplot(data=df, x='frame_rate', y='network_load',
                    hue='station_count', size='throughput', ax=axes3[1,1])
    axes3[1,1].set_title('Network Load vs Frame Rate')
    axes3[1,1].set_ylabel('Network Load (frames/s)')
    
    plt.tight_layout()
    plt.savefig('results/plots/frame_rate_analysis.png')
    plt.close()

if __name__ == "__main__":
    analyze_key_factors() 