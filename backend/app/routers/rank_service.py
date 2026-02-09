def predict_rank(avg_score_percent):
    avg_percent = (total_marks / max_marks) * 100


    if avg_score_percent >= 75:
        return "Top 500 Rank Range"
    elif avg_score_percent >= 65:
        return "Top 1500 Rank Range"
    elif avg_score_percent >= 55:
        return "Interview Borderline"
    else:
        return "Needs Improvement"
