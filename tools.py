import csv
import json
import os 

def aggregate_metrics(data_dir="mock_data"):
    filepath = os.path.join(data_dir, "metrics.csv")
    rows = [] 
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)   # DictReader turns each row into a dictionary
        for row in reader:
            rows.append(row)
 
    pre  = rows[:7]
    post = rows[7:]
 
    def avg(data, col):
        return sum(float(r[col]) for r in data) / len(data)

    return {
        "total_days": len(rows),
        "pre_launch_days": len(pre),
        "post_launch_days": len(post),
        "post_launch_avg": {
            "activation_rate":       round(avg(post, "activation_rate"), 3),
            "dau_wau":               round(avg(post, "dau_wau"), 3),
            "d1_retention":          round(avg(post, "d1_retention"), 3),
            "crash_rate":            round(avg(post, "crash_rate"), 4),
            "api_latency_p95":       round(avg(post, "api_latency_p95"), 1),
            "payment_success_rate":  round(avg(post, "payment_success_rate"), 3),
            "support_tickets":       round(avg(post, "support_tickets"), 1),
            "churn_rate":            round(avg(post, "churn_rate"), 4),
        },
        "pre_launch_avg": {
            "activation_rate":       round(avg(pre, "activation_rate"), 3),
            "dau_wau":               round(avg(pre, "dau_wau"), 3),
            "d1_retention":          round(avg(pre, "d1_retention"), 3),
            "crash_rate":            round(avg(pre, "crash_rate"), 4),
            "api_latency_p95":       round(avg(pre, "api_latency_p95"), 1),
            "payment_success_rate":  round(avg(pre, "payment_success_rate"), 3),
            "support_tickets":       round(avg(pre, "support_tickets"), 1),
            "churn_rate":            round(avg(pre, "churn_rate"), 4),
        }
    }
 

def detect_anomalies(data_dir="mock_data"):
    summary = aggregate_metrics(data_dir)
    pre  = summary["pre_launch_avg"]
    post = summary["post_launch_avg"]

    anomalies = []
 
    worse_if_higher = ["crash_rate", "api_latency_p95", "support_tickets", "churn_rate"]
 
    worse_if_lower  = ["activation_rate", "dau_wau", "d1_retention", "payment_success_rate"]

    for metric in worse_if_higher:
        pre_val  = pre[metric]
        post_val = post[metric]
        if pre_val > 0:
            change_pct = ((post_val - pre_val) / pre_val) * 100
            if change_pct > 20:    
                anomalies.append({
                    "metric": metric,
                    "pre":    pre_val,
                    "post":   post_val,
                    "change": f"+{round(change_pct)}%",
                    "direction": "increased (bad)"
                })

    for metric in worse_if_lower:
        pre_val  = pre[metric]
        post_val = post[metric]
        if pre_val > 0:
            change_pct = ((pre_val - post_val) / pre_val) * 100
            if change_pct > 10:    
                anomalies.append({
                    "metric": metric,
                    "pre":    pre_val,
                    "post":   post_val,
                    "change": f"-{round(change_pct)}%",
                    "direction": "decreased (bad)"
                })

    return {
        "anomaly_count": len(anomalies),
        "anomalies": anomalies
    } 

def analyse_sentiment(data_dir="mock_data"):
    filepath = os.path.join(data_dir, "user_feedback.json")

    with open(filepath) as f:
        feedback = json.load(f)    

    total     = len(feedback)
    positive  = sum(1 for f in feedback if f["sentiment"] == "positive")
    negative  = sum(1 for f in feedback if f["sentiment"] == "negative")
    neutral   = sum(1 for f in feedback if f["sentiment"] == "neutral")
 
    themes = {"crash": 0, "slow": 0, "payment": 0, "cancel": 0, "support": 0}
    keywords = {
        "crash":   ["crash", "freeze", "freezing", "closes"],
        "slow":    ["slow", "latency", "timeout", "loading", "forever"],
        "payment": ["payment", "checkout", "purchase", "sale"],
        "cancel":  ["cancel", "uninstall", "switching", "rolled back"],
        "support": ["support", "ticket", "response", "team"]
    }

    for entry in feedback:
        if entry["sentiment"] == "negative":
            text = entry["text"].lower()
            for theme, words in keywords.items():
                if any(word in text for word in words):
                    themes[theme] += 1

    return {
        "total_feedback": total,
        "sentiment_breakdown": {
            "positive": positive,
            "negative": negative,
            "neutral":  neutral
        },
        "negative_themes": themes,
        "nps_proxy": round(((positive - negative) / total) * 100, 1)
    }

 

def compare_trend(data_dir="mock_data"):
    summary = aggregate_metrics(data_dir)
    pre  = summary["pre_launch_avg"]
    post = summary["post_launch_avg"]

    def pct_change(before, after):
        if before == 0:
            return "N/A"
        return round(((after - before) / before) * 100, 1)

    return {
        "crash_rate_change_pct":           pct_change(pre["crash_rate"],           post["crash_rate"]),
        "api_latency_change_pct":          pct_change(pre["api_latency_p95"],       post["api_latency_p95"]),
        "support_tickets_change_pct":      pct_change(pre["support_tickets"],       post["support_tickets"]),
        "churn_rate_change_pct":           pct_change(pre["churn_rate"],            post["churn_rate"]),
        "activation_rate_change_pct":      pct_change(pre["activation_rate"],       post["activation_rate"]),
        "payment_success_rate_change_pct": pct_change(pre["payment_success_rate"],  post["payment_success_rate"]),
        "d1_retention_change_pct":         pct_change(pre["d1_retention"],          post["d1_retention"]),
    }
