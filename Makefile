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
	@`ps -ax | grep get_prices | awk '{print $1}' | xargs kill -9`
price-check:
	@poetry run python3 price_check.py
strat-check:
	@poetry run python3 strategy_checker.py
	@poetry run python3 main.py
nuke:
	@echo "Deleting env"
	@sudo rm -r `poetry env info -p`
	@rm poetry.lock
main:
	@poetry run python3 main.py
strat-check2:
	@poetry run python3 strat_check2.py
	@poetry run python3 main.py