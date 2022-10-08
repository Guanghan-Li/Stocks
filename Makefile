run:
	@poetry run python3 get_prices.py
delete:
	@poetry run python3 delete_data.py
stop:
	@./stop_everything.sh