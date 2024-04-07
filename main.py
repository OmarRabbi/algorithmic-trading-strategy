from trading_strategy import TradingStrategy

if __name__ == "__main__":
    try:
        strategy = TradingStrategy("TSLA", "2022-01-01", "2024-03-31")
        strategy.download_data()
        strategy.clean_data()
        strategy.compute_moving_averages()
        strategy.identify_golden_cross()
        strategy.determine_max_shares()
        strategy.execute_trade()
        strategy.calculate_total_profit_loss()
    except Exception as e:
        print("An error occurred:", str(e))
