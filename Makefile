get-prices:
	@poetry run python3 get_prices.py
get-reports:
	@poetry run python3 get_reports.py
transfer:
	@poetry run python3 transfer.py
strategy:
	@poetry run python3 portfolio_checker.py
delete:
	@rm -f errors/*
	@rm -f problem_json/*
	@echo "Now removing DB"
	@poetry run python3 delete_data.py
stop:
	@ps -ef | grep stock- | awk '{print $2}' | xargs kill -9
price-check:
	@poetry run python3 price_check.py
