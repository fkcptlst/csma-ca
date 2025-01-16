import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_all_results, parse_filename

def analyze_temporal_patterns():
    """Analyze how metrics change over time"""
    results = load_all_results()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    
    # Select a representative configuration for temporal analysis
    example_key = list(results.keys())[0]
    df = results[example_key]
    
    # Plot 1: Throughput over time
    axes[0,0].plot(df['current'], df['bps'], label='Actual')
    axes[0,0].plot(df['current'], df['max_bps'], label='Theoretical Max', linestyle='--')
    axes[0,0].set_title('Throughput Over Time')
    axes[0,0].set_xlabel('Time (ms)')
    axes[0,0].set_ylabel('Throughput (Kbps)')
    axes[0,0].legend()
    axes[0,0].grid(True)
    
    # Plot 2: Collision rate evolution
    axes[0,1].plot(df['current'], df['collision_rate'] * 100)
    axes[0,1].set_title('Collision Rate Evolution')
    axes[0,1].set_xlabel('Time (ms)')
    axes[0,1].set_ylabel('Collision Rate (%)')
    axes[0,1].grid(True)
    
    # Plot 3: Frame count on air
    axes[1,0].plot(df['current'], df['frame_on_air'])
    axes[1,0].set_title('Frames in Transmission')
    axes[1,0].set_xlabel('Time (ms)')
    axes[1,0].set_ylabel('Frame Count')
    axes[1,0].grid(True)
    
    # Plot 4: Cumulative sent vs processed frames
    axes[1,1].plot(df['current'], df['sent'].cumsum(), label='Sent')
    axes[1,1].plot(df['current'], (df['processed']/df['data_rate']).cumsum(), label='Processed')
    axes[1,1].set_title('Cumulative Frame Statistics')
    axes[1,1].set_xlabel('Time (ms)')
    axes[1,1].set_ylabel('Frame Count')
    axes[1,1].legend()
    axes[1,1].grid(True)
    
    plt.tight_layout()
    plt.savefig('results/plots/temporal_patterns.png')
    plt.close()

if __name__ == "__main__":
    analyze_temporal_patterns() 