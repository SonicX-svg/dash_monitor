# dash_monitor
Monitoring using the python dash library using metrics from the iostat, nmon, sar utilities<br>
1. Getting metrics for the iostat graph:
  Launch graph_app.py and then clean.sh. (change the collection time in graph_app.py )
2. Getting nmon metrics. Run it in the terminal:
   pyNmonAnalyzer -c -o testOut -i <your_file>.nmon
   and get the csv folder from TestOut. Done!
3. Запускай graph_app.py


or just download it to check
