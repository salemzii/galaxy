import pandas as pd
import matplotlib.pyplot as plt

class EarthVisualizer():
    data  = "archive/earthquake_data.csv"

    def __init__(self) -> None:
        self.df = pd.read_csv(self.data)

    def magnitude_of_quakes(self):
        plt.hist(self.df['magnitude'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Magnitude')
        plt.ylabel('Frequency')
        plt.title('Distribution of Earthquake Magnitudes')
        plt.show()

    def times_series_plot(self):
        self.df['date_time'] = pd.to_datetime(self.df['date_time'])
        self.df.set_index('date_time', inplace=True)
        self.df['magnitude'].plot(figsize=(12, 6))
        plt.xlabel('Date')
        plt.ylabel('Magnitude')
        plt.title('Earthquake Magnitude Over Time')
        plt.show()
    
    def earthquakes_23(self):
        self.df['date_time'] = pd.to_datetime(self.df['date_time'])
        earthquakes_2023 = self.df[self.df['date_time'].dt.year == 2023]
        return earthquakes_2023
    
    def scatter_plot_quakes(self):
        plt.scatter(self.df['longitude'], self.df['latitude'], c=self.df['magnitude'], cmap='viridis', alpha=0.5)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Earthquake Locations and Magnitudes')
        plt.colorbar(label='Magnitude')
        plt.show()  

ev = EarthVisualizer()

print(ev.scatter_plot_quakes())
