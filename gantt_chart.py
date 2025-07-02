import pandas as pd

def load_data(file_path):
    """
    Load data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file.
        
    Returns:
        dict: Dictionary containing dataframes for each sheet.
    """
    sheets = pd.read_excel(file_path, sheet_name=None)
    return sheets

def draw_gantt_chart(operation_df, assembly_df):
    """
    Draw a Gantt chart for operations and assemblies.
    
    Args:
        operation_df (pd.DataFrame): DataFrame containing operation data.
        assembly_df (pd.DataFrame): DataFrame containing assembly data.
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot operations
    for _, row in operation_df.iterrows():
        ax.barh(row['Part'], row['End'] - row['Start'], left=row['Start'], label=f"Op {row['Operation']}")

    # Plot assemblies
    for _, row in assembly_df.iterrows():
        ax.barh(row['Assembly'], row['End'] - row['Start'], left=row['Start'], color='orange', alpha=0.5, label='Assembly')

    ax.set_xlabel('Time')
    ax.set_ylabel('Parts/Assemblies')
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.title('Gantt Chart of Operations and Assemblies')
    plt.legend()
    plt.tight_layout()
    plt.show()
def main():
    # Load data from Excel file
    file_path = 'operating_times.xlsx'
    sheets = load_data(file_path)

    # Extract operation and assembly data
    operation_df = sheets['operation_times']
    assembly_df = sheets['assembly_times']

    # Draw Gantt chart
    draw_gantt_chart(operation_df, assembly_df)