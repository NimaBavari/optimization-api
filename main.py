import random
import time

from flask import Flask, Response, jsonify, request

from optimization_lib import benchmark_stats, efficient, naive

app = Flask(__name__)


@app.route("/optimize/efficient")
def get_efficient_optimization():
    """Incoming request shape:
    ```
    {
        "lists":    list of lists, each containing ints,
        "m":        int,
        "f":        str (lambda definition)
    }
    ```
    """
    lists = request.json["lists"]
    m = request.json["m"]
    f = eval(request.json["f"])
    try:
        result = efficient(lists, m, f)
    except Exception:
        return Response("Bad request", status=400)
    return jsonify({"result": result})


@app.route("/optimize/naive")
def get_naive_optimization():
    """Incoming request shape:
    ```
    {
        "lists":    list of lists, each containing ints,
        "m":        int,
        "f":        str (lambda definition)
    }
    ```
    """
    lists = request.json["lists"]
    m = request.json["m"]
    f = eval(request.json["f"])
    try:
        result = naive(lists, m, f)
    except Exception:
        return Response("Bad request", status=400)
    return jsonify({"result": result})


@app.route("/benchmark/efficient")
def get_efficient_benchmark():
    """Incoming request shape:
    ```
    {
        "num_lists":    int,
        "num_elements": int,
        "m":            int,
        "f":            str (lambda definition),
        "replications": int
    }
    ```
    """
    num_lists = request.json["num_lists"]
    num_elements = request.json["num_elements"]
    m = request.json["m"]
    f = eval(request.json["f"])
    replications = request.json["replications"]
    try:
        resp = benchmark_stats(num_lists, num_elements, m, f, replications, efficient)
    except Exception:
        return Response("Bad request", status=400)
    return jsonify(resp)


@app.route("/benchmark/naive")
def get_naive_benchmark():
    """Incoming request shape:
    ```
    {
        "num_lists":    int,
        "num_elements": int,
        "m":            int,
        "f":            str (lambda definition),
        "replications": int
    }
    ```
    """
    num_lists = request.json["num_lists"]
    num_elements = request.json["num_elements"]
    m = request.json["m"]
    f = eval(request.json["f"])
    replications = request.json["replications"]
    try:
        resp = benchmark_stats(num_lists, num_elements, m, f, replications, naive)
    except Exception:
        return Response("Bad request", status=400)
    return jsonify(resp)


@app.route("/perf-comparison/<int:num_lists>")
def get_perf_comparison(num_lists):
    """Incoming request shape:
    ```
    {
        "num_elements": int,
        "m":            int,
        "f":            str (lambda definition)
    }
    ```
    """
    num_elements = request.json["num_elements"]
    m = request.json["m"]
    f = eval(request.json["f"])
    rand_lists = [random.sample(range(1, 10**9 + 1), num_elements)] + [
        random.sample(range(1, 10**9 + 1), random.randint(1, 10)) for _ in range(num_lists - 1)
    ]
    try:
        efficient_start = time.perf_counter()
        _ = efficient(rand_lists, m, f)
        efficient_perf = time.perf_counter() - efficient_start

        naive_start = time.perf_counter()
        _ = naive(rand_lists, m, f)
        naive_perf = time.perf_counter() - naive_start
    except Exception:
        return Response("Bad request", status=400)
    return jsonify(
        {
            "num_lists": num_lists,
            "efficient_perf": efficient_perf,
            "naive_perf": naive_perf,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
