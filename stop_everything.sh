ps aux | grep python | cut -d' ' -f4 | xargs kill -9
ps aux | grep python | cut -d' ' -f5| xargs kill -9
