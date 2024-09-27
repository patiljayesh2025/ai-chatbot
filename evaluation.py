from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# I uploaded my resume and asked some questions to chatbot
questions = [
    "What is the contact number of jayesh patil ?",
    "Where did jayesh patil study ?",
    "How many years of experience jayesh patil has ?",
    "what is the email address of jayesh patil ?",
    "What all certifications jayesh patil has cleared ?",
    "What is qualification of jayesh patil ?",
]
ground_truth = [
    "+91-8329519847",
    "Government College Of Engineering and Research,Pune.",
    "3+ years",
    "epatiljayesh2025@gmail.com",
    "GCP - Associate Cloud Engineer AWS - Cloud Practitioner",
    "Bachelor of Engineering in Computer Science",
]
predicted_answers = [
    "+91-8329519847",
    "Government College Of Engineering and Research,Pune.",
    "3+ years",
    "patiljayesh2025@gmail.com",
    "GCP - Associate Cloud Engineer AWS - Cloud Practitioner",
    "Bachelor of Engineering in Computer Science",
]

acc = accuracy_score(ground_truth, predicted_answers)

# Calculate precision, recall, f1 (if binary or multi-class)
precision = precision_score(ground_truth, predicted_answers, average="macro")
recall = recall_score(ground_truth, predicted_answers, average="macro")
f1 = f1_score(ground_truth, predicted_answers, average="macro")

# Calculate BLEU and ROUGE for text comparison
bleu_scores = [
    sentence_bleu([truth.split()], pred.split())
    for truth, pred in zip(ground_truth, predicted_answers)
]
rouge = Rouge()
rouge_scores = [
    rouge.get_scores(pred, truth)
    for pred, truth in zip(predicted_answers, ground_truth)
]


report = {
    "Accuracy": acc,
    "Precision": precision,
    "Recall": recall,
    "F1-Score": f1,
    "Average BLEU": sum(bleu_scores) / len(bleu_scores),
    "Average ROUGE": sum([r[0]["rouge-l"]["f"] for r in rouge_scores])
    / len(rouge_scores),
}
print(report)
