import timeit

def benchmark_code(code_snippet, test_input=""):
    try:
        setup = f"{test_input}\n{code_snippet}"
        time_taken = timeit.timeit(stmt=code_snippet, number=10, globals=globals())
        return {
            "execution_time": round(time_taken, 4),
            "remarks": "Benchmark completed successfully."
        }
    except Exception as e:
        return {"error": f"Benchmark failed: {e}"}