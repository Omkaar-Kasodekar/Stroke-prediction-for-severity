import httpx


def main() -> None:
    base = "http://127.0.0.1:8000"

    # Simple GET endpoints
    for path in ["/health", "/openapi.json"]:
        url = base + path
        try:
            resp = httpx.get(url, timeout=5.0)
            print(f"{path} -> {resp.status_code}")
            print(resp.text[:400])
            print("-" * 40)
        except Exception as exc:
            print(f"{path} ERROR: {exc}")

    # Predict endpoint (POST)
    payload = {
        "age": 70,
        "bmi": 33.2,
        "avg_glucose_level": 165,
        "hypertension": 1,
        "heart_disease": 1,
    }
    try:
        resp = httpx.post(base + "/predict", json=payload, timeout=10.0)
        print("/predict ->", resp.status_code)
        print(resp.text[:400])
        print("-" * 40)
    except Exception as exc:
        print("/predict ERROR:", exc)


if __name__ == "__main__":
    main()


