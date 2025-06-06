from collections import defaultdict

def simulate_trend(raw_data):
    trend = defaultdict(list)
    for timestamp, rating in raw_data:
        date = timestamp.split(" ")[0]
        trend[date].append(rating)

    return [{"day": day, "score": sum(vals) / len(vals)} for day, vals in sorted(trend.items())]
