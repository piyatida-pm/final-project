"""
Statistics analyzer for the pizza game.
Reads CSV data and provides analysis for visualization.
Supports loading single or multiple CSV files from collecting_data folder.
"""
import csv
import os
from collections import defaultdict

class StatsAnalyzer:
    """Analyzes game statistics from CSV files"""
    
    def __init__(self, csv_filename=None, load_all_from_folder=False, folder_path=None):
        """
        Initialize stats analyzer.
        
        Args:
            csv_filename: Single CSV file to load
            load_all_from_folder: If True, load all CSV files from folder
            folder_path: Path to collecting_data folder. If None, auto-detect
        """
        self.csv_filename = csv_filename
        self.data = []
        self.loaded_files = []
        self.data_source = "Single Session"
        
        if load_all_from_folder:
            # Load all CSV files from collecting_data folder
            if folder_path is None:
                # Auto-detect collecting_data folder
                project_root = os.path.dirname(os.path.abspath(__file__))
                folder_path = os.path.join(project_root, "collecting_data")
            self.load_all_from_folder(folder_path)
        elif csv_filename:
            self.load_data()
    
    def load_data(self):
        """Load data from single CSV file"""
        self.data = []
        self.loaded_files = []
        if os.path.exists(self.csv_filename):
            try:
                with open(self.csv_filename, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.data.append(row)
                self.loaded_files.append(os.path.basename(self.csv_filename))
                self.data_source = f"Session: {os.path.basename(self.csv_filename)}"
            except:
                pass
    
    def load_all_from_folder(self, folder_path):
        """Load and aggregate data from all CSV files in folder"""
        self.data = []
        self.loaded_files = []
        
        if not os.path.exists(folder_path):
            return
        
        try:
            csv_files = [f for f in os.listdir(folder_path) if f.startswith('pizza_stats_') and f.endswith('.csv')]
            csv_files.sort()  # Sort chronologically
            
            for csv_file in csv_files:
                filepath = os.path.join(folder_path, csv_file)
                try:
                    with open(filepath, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.data.append(row)
                    self.loaded_files.append(csv_file)
                except:
                    pass
            
            file_count = len(self.loaded_files)
            self.data_source = f"All Sessions ({file_count} games)" if file_count > 0 else "No data"
        except:
            pass
    
    def get_total_orders(self):
        """Get total number of orders completed"""
        return len(self.data)
    
    def get_total_revenue(self):
        """Get total revenue from all orders"""
        total = 0
        for row in self.data:
            try:
                total += float(row.get('ItemPrice', 0))
            except:
                pass
        return total
    
    def get_average_price(self):
        """Get average price per order"""
        if len(self.data) == 0:
            return 0
        return self.get_total_revenue() / len(self.data)
    
    def get_topping_frequency(self):
        """Get frequency of each topping used"""
        topping_count = defaultdict(int)
        for row in self.data:
            toppings_used = int(row.get('ToppingsUsed', 0))
            topping_count['Total Toppings'] += toppings_used
        return dict(topping_count)
    
    def get_drink_frequency(self):
        """Get frequency of each drink type"""
        drink_count = defaultdict(int)
        for row in self.data:
            drink_type = row.get('DrinkType', 'None')
            drink_count[drink_type] += 1
        return dict(sorted(drink_count.items(), key=lambda x: x[1], reverse=True))
    
    def get_accuracy_stats(self):
        """Get order accuracy statistics"""
        total = len(self.data)
        if total == 0:
            return {'Correct': 0, 'Percentage': 0}
        
        correct = sum(1 for row in self.data if row.get('OrderAccuracy', '') == 'Correct')
        percentage = (correct / total) * 100
        
        return {
            'Correct': correct,
            'Total': total,
            'Incorrect': total - correct,
            'Percentage': percentage
        }
    
    def get_time_statistics(self):
        """Get time taken statistics"""
        times = []
        for row in self.data:
            try:
                time_taken = int(row.get('TimeTaken', 0))
                times.append(time_taken)
            except:
                pass
        
        if not times:
            return {'min': 0, 'max': 0, 'avg': 0, 'count': 0}
        
        return {
            'min': min(times),
            'max': max(times),
            'avg': sum(times) / len(times),
            'count': len(times)
        }
    
    def get_daily_stats(self):
        """Get statistics grouped by day"""
        daily_data = defaultdict(lambda: {'orders': 0, 'revenue': 0, 'correct': 0})
        
        for row in self.data:
            day = row.get('Day', '1')
            try:
                revenue = float(row.get('ItemPrice', 0))
                daily_data[day]['orders'] += 1
                daily_data[day]['revenue'] += revenue
                if row.get('OrderAccuracy', '') == 'Correct':
                    daily_data[day]['correct'] += 1
            except:
                pass
        
        return dict(sorted(daily_data.items()))
    
    def get_data_source(self):
        """Get description of loaded data source"""
        return self.data_source
    
    def get_loaded_files(self):
        """Get list of loaded CSV files"""
        return self.loaded_files
