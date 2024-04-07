import yfinance as yf

class TradingStrategy:
    def __init__(self, symbol, from_date, to_date, initial_budget=5000):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.initial_budget = initial_budget
        self.data = None
        self.max_shares = None
        self.position = 0
        self.profits_losses = []

    def download_data(self):
        try:
            self.data = yf.download(self.symbol, start=self.from_date, end=self.to_date)
            print("Data downloaded successfully!")
        except Exception as e:
            print("Error downloading data:", str(e))
            self.data = None

    def clean_data(self):
        if self.data is not None:
            try:
                self.data = self.data[~self.data.index.duplicated(keep='first')]
                self.data = self.data.ffill()
                print("Data cleaned successfully!")
            except Exception as e:
                print("Error cleaning data:", str(e))
        else:
            print("No data to clean. Please download data first.")

    def compute_moving_averages(self):
        if self.data is not None:
            try:
                self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
                self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
                print("Moving averages computed successfully!")
            except Exception as e:
                print("Error computing moving averages:", str(e))
        else:
            print("No data available. Please download data first.")

    def identify_golden_cross(self):
        if self.data is not None:
            try:
                self.data['Signal'] = 0
                self.data.loc[self.data['MA50'] > self.data['MA200'], 'Signal'] = 1
                self.data['Position'] = self.data['Signal'].diff()
                print("Golden cross identified successfully!")
            except Exception as e:
                print("Error identifying golden cross:", str(e))
        else:
            print("No data available. Please download data first.")

    def determine_max_shares(self):
        if self.data is not None:
            try:
                available_budget_per_share = self.initial_budget / self.data['Close'].iloc[0]
                self.max_shares = int(available_budget_per_share)
                print("Maximum quantity of shares determined successfully!")
            except Exception as e:
                print("Error determining maximum shares:", str(e))
        else:
            print("No data available. Please download data first.")

    def execute_trade(self):
        if self.data is not None:
            try:
                for _, row in self.data.iterrows():
                    if row['Position'] == 1 and self.position == 0:
                        self.position = 1
                        print("Buy: {} shares per at {}".format(self.max_shares, row['Close']))
                        buy_price = row['Close']
                    elif row['Position'] == -1 and self.position == 1:
                        self.position = 0
                        print("Sell: {} shares per at {}".format(self.max_shares, row['Close']))
                        sell_price = row['Close']
                        trade_profit_loss = (sell_price - buy_price) * self.max_shares
                        self.profits_losses.append(trade_profit_loss)

                if self.data['Position'].iloc[-1] == 1:
                    self.position = 0
                    print("Forcefully closing the position at the end.")
                print("Trades executed successfully!")
            except Exception as e:
                print("Error executing trades:", str(e))
        else:
            print("No data available. Please download data first.")

    def calculate_total_profit_loss(self):
        if self.profits_losses:
            try:
                total_profit_loss = sum(self.profits_losses)
                if total_profit_loss >= 0:
                    print("Total profit: ${}".format(total_profit_loss))
                else:
                    print("Total loss: ${}".format(abs(total_profit_loss)))
            except Exception as e:
                print("Error calculating total profit/loss:", str(e))
        else:
            print("No trades executed yet.")

# import yfinance as yf
# import pandas as pd

# class TradingStrategy:
#     def __init__(self, symbol, from_date, to_date, initial_budget=5000):
#         self.symbol = symbol
#         self.from_date = from_date
#         self.to_date = to_date
#         self.initial_budget = initial_budget
#         self.data = None
#         self.max_shares = None
#         self.position = 0
#         self.profits_losses = []

#     def download_data(self):
#         try:
#             self.data = yf.download(self.symbol, start=self.from_date, end=self.to_date)
#             print("Data downloaded successfully!")
#         except Exception as e:
#             print("Error downloading data:", str(e))
#             self.data = None

#     def clean_data(self):
#         if self.data is not None:
#             try:
#                 self.data = self.data[~self.data.index.duplicated(keep='first')]
#                 self.data = self.data.ffill()
#                 print("Data cleaned successfully!")
#             except Exception as e:
#                 print("Error cleaning data:", str(e))
#         else:
#             print("No data to clean. Please download data first.")

#     def compute_moving_averages(self):
#         if self.data is not None:
#             try:
#                 self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
#                 self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
#                 print("Moving averages computed successfully!")
#             except Exception as e:
#                 print("Error computing moving averages:", str(e))
#         else:
#             print("No data available. Please download data first.")

#     def identify_golden_cross(self):
#         if self.data is not None:
#             try:
#                 self.data['Signal'] = 0
#                 self.data.loc[self.data['MA50'] > self.data['MA200'], 'Signal'] = 1
#                 self.data['Position'] = self.data['Signal'].diff()
#                 print("Golden cross identified successfully!")
#             except Exception as e:
#                 print("Error identifying golden cross:", str(e))
#         else:
#             print("No data available. Please download data first.")

#     def determine_max_shares(self):
#         if self.data is not None:
#             try:
#                 available_budget_per_share = self.initial_budget / self.data['Close'].iloc[0]
#                 self.max_shares = int(available_budget_per_share)
#                 print("Maximum quantity of shares determined successfully!")
#             except Exception as e:
#                 print("Error determining maximum shares:", str(e))
#         else:
#             print("No data available. Please download data first.")

#     def execute_trade(self):
#         if self.data is not None:
#             try:
#                 for _, row in self.data.iterrows():
#                     if row['Position'] == 1 and self.position == 0:
#                         self.position = 1
#                         print("Buy: {} shares at {}".format(self.max_shares, row['Close']))
#                     elif row['Position'] == -1 and self.position == 1:
#                         self.position = 0
#                         print("Sell: {} shares at {}".format(self.max_shares, row['Close']))
#                         trade_profit_loss = (row['Close'] - self.data['Close'].iloc[-1]) * self.max_shares
#                         self.profits_losses.append(trade_profit_loss)

#                 if self.data['Position'].iloc[-1] == 1:
#                     self.position = 0
#                     print("Forcefully closing the position at the end.")
#                 print("Trades executed successfully!")
#             except Exception as e:
#                 print("Error executing trades:", str(e))
#         else:
#             print("No data available. Please download data first.")

#     def calculate_total_profit_loss(self):
#         if self.profits_losses:
#             try:
#                 total_profit_loss = sum(self.profits_losses)
#                 if total_profit_loss >= 0:
#                     print("Total profit: ${}".format(total_profit_loss))
#                 else:
#                     print("Total loss: ${}".format(abs(total_profit_loss)))
#             except Exception as e:
#                 print("Error calculating total profit/loss:", str(e))
#         else:
#             print("No trades executed yet.")
