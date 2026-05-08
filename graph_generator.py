"""
Graph generator for pizza game statistics using matplotlib.
Converts matplotlib figures to pygame-compatible surfaces.
"""
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
import io
from PIL import Image
import numpy as np

class GraphGenerator:
    """Generates matplotlib graphs for game statistics"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        plt.style.use('default')
    
    def fig_to_pygame_surface(self, fig):
        """Convert matplotlib figure to pygame surface"""
        try:
            # Save figure to bytes buffer
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            buf.seek(0)
            
            # Load image with PIL
            img = Image.open(buf)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert PIL image to pygame surface
            img_data = img.tobytes()
            surf = pygame.image.fromstring(img_data, img.size, "RGB")
            
            plt.close(fig)
            buf.close()
            return surf
        except Exception as e:
            print(f"Error converting figure to surface: {e}")
            import traceback
            traceback.print_exc()
            plt.close(fig)
            return None
    
    def generate_revenue_chart(self, stats_analyzer):
        """Generate revenue overview chart"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.patch.set_facecolor('#F5F5DC')  # CREAM color
            
            # Total Revenue
            total_revenue = stats_analyzer.get_total_revenue()
            ax1.bar(['Total Revenue'], [total_revenue], color='#FF8C00', width=0.5)
            ax1.set_ylabel('Amount ($)', fontsize=10, fontweight='bold')
            ax1.set_title('Total Revenue', fontsize=12, fontweight='bold')
            ax1.set_ylim(0, max(total_revenue * 1.2, 100))
            for rect in ax1.patches:
                height = rect.get_height()
                ax1.text(rect.get_x() + rect.get_width()/2., height,
                        f'${height:.2f}', ha='center', va='bottom', fontweight='bold')
            
            # Average Price
            avg_price = stats_analyzer.get_average_price()
            ax2.bar(['Average Price'], [avg_price], color='#32B432', width=0.5)
            ax2.set_ylabel('Amount ($)', fontsize=10, fontweight='bold')
            ax2.set_title('Average Price per Order', fontsize=12, fontweight='bold')
            ax2.set_ylim(0, max(avg_price * 1.5, 50))
            for rect in ax2.patches:
                height = rect.get_height()
                ax2.text(rect.get_x() + rect.get_width()/2., height,
                        f'${height:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating revenue chart: {e}")
            return None
    
    def generate_orders_chart(self, stats_analyzer):
        """Generate total orders display"""
        try:
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor('#F5F5DC')
            
            total_orders = stats_analyzer.get_total_orders()
            ax.bar(['Orders Completed'], [total_orders], color='#DC143C', width=0.4)
            ax.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
            ax.set_title('Total Orders Completed', fontsize=13, fontweight='bold')
            ax.set_ylim(0, max(total_orders * 1.3, 10))
            
            for rect in ax.patches:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating orders chart: {e}")
            return None
    
    def generate_accuracy_chart(self, stats_analyzer):
        """Generate order accuracy pie chart"""
        try:
            accuracy = stats_analyzer.get_accuracy_stats()
            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_facecolor('#F5F5DC')
            
            sizes = [accuracy['Correct'], accuracy['Incorrect']]
            labels = [f"Correct\n({accuracy['Correct']})", f"Incorrect\n({accuracy['Incorrect']})"]
            colors = ['#32B432', '#DC143C']
            explode = (0.1, 0)
            
            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                  shadow=True, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
            ax.set_title('Order Accuracy', fontsize=13, fontweight='bold', pad=20)
            
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating accuracy chart: {e}")
            return None
    
    def generate_drink_frequency_chart(self, stats_analyzer):
        """Generate drink frequency bar chart"""
        try:
            drink_freq = stats_analyzer.get_drink_frequency()
            if not drink_freq:
                return None
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#F5F5DC')
            
            drinks = list(drink_freq.keys())
            counts = list(drink_freq.values())
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
            
            bars = ax.bar(drinks, counts, color=colors[:len(drinks)], edgecolor='black', linewidth=1.5)
            ax.set_ylabel('Number of Orders', fontsize=11, fontweight='bold')
            ax.set_xlabel('Drink Type', fontsize=11, fontweight='bold')
            ax.set_title('Drink Frequency', fontsize=13, fontweight='bold')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating drink chart: {e}")
            return None
    
    def generate_time_statistics_chart(self, stats_analyzer):
        """Generate time statistics display"""
        try:
            time_stats = stats_analyzer.get_time_statistics()
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#F5F5DC')
            
            time_labels = ['Min', 'Avg', 'Max']
            time_values = [time_stats['min'], time_stats['avg'], time_stats['max']]
            colors = ['#9370DB', '#FFD700', '#FF6347']
            
            bars = ax.bar(time_labels, time_values, color=colors, edgecolor='black', linewidth=1.5)
            ax.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
            ax.set_title('Time Statistics', fontsize=13, fontweight='bold')
            ax.set_ylim(0, max(time_values) * 1.2 if time_values else 100)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}s', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating time statistics chart: {e}")
            return None
    
    def generate_daily_summary_chart(self, stats_analyzer):
        """Generate daily summary line chart"""
        try:
            daily_stats = stats_analyzer.get_daily_stats()
            if not daily_stats:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#F5F5DC')
            
            days = [int(day) for day in daily_stats.keys()]
            revenues = [daily_stats[str(day)]['revenue'] for day in days]
            
            ax.plot(days, revenues, marker='o', linewidth=2.5, markersize=8, 
                   color='#FF8C00', markerfacecolor='#FFD700', markeredgewidth=2, markeredgecolor='#FF8C00')
            ax.fill_between(days, revenues, alpha=0.3, color='#FF8C00')
            ax.set_xlabel('Day', fontsize=11, fontweight='bold')
            ax.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold')
            ax.set_title('Revenue Trend Over Days', fontsize=13, fontweight='bold')
            ax.set_xticks(days)
            ax.grid(True, alpha=0.3)
            
            for day, revenue in zip(days, revenues):
                ax.text(day, revenue, f'${revenue:.0f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating daily summary chart: {e}")
            return None
    
    def generate_topping_statistics_chart(self, stats_analyzer):
        """Generate topping statistics display"""
        try:
            topping_freq = stats_analyzer.get_topping_frequency()
            if not topping_freq:
                return None
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#F5F5DC')
            
            toppings = list(topping_freq.keys())
            counts = list(topping_freq.values())
            colors = ['#FF69B4', '#32CD32', '#1E90FF', '#FFD700', '#FF6347', '#00CED1']
            
            bars = ax.bar(toppings, counts, color=colors[:len(toppings)], edgecolor='black', linewidth=1.5)
            ax.set_ylabel('Total Used', fontsize=11, fontweight='bold')
            ax.set_title('Topping Usage Statistics', fontsize=13, fontweight='bold')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return self.fig_to_pygame_surface(fig)
        except Exception as e:
            print(f"Error generating topping chart: {e}")
            return None
