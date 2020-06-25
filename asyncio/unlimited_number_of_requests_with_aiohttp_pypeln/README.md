# Making an Unlimited Number of Requests with Python aiohttp + pypeln
> [origin](https://medium.com/@cgarciae/making-an-infinite-number-of-requests-with-python-aiohttp-pypeln-3a552b97dc95)

```bash

➜ bash timed.sh python client-async-sem.py 100000
Memory usage: 352684KB  Time: 154.87 seconds    CPU usage: 38%
➜ bash timed.sh python client-async-as-completed.py 100000
Memory usage: 57548KB   Time: 154.91 seconds    CPU usage: 100%
➜ bash timed.sh python client-task-pool.py 100000
Memory usage: 58188KB   Time: 153.40 seconds    CPU usage: 36%
➜ bash timed.sh python client-pypeln-io.py 100000
Memory usage: 63624KB   Time: 154.39 seconds    CPU usage: 37%

```