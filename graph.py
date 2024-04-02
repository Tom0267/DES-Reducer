import matplotlib.pyplot as plt
averages = [4.14, 1, 4.86, 1, 4, 1, 4.71, 1.43, 4.57, 1]

# Enhancing the plot with descriptive labels for each question

# Redefining the question descriptions for clarity
question_descriptions = [
    'Q1: Frequent use likelihood',
    'Q2: Unnecessarily complex',
    'Q3: Ease of use',
    'Q4: Need for assistance',
    'Q5: Well-integrated functions',
    'Q6: Inconsistency issues',
    'Q7: Quick learning curve',
    'Q8: Cumbersome to use',
    'Q9: Confidence in use',
    'Q10: Pre-use learning required'
]

plt.figure(figsize=(12, 8))
bars = plt.bar(question_descriptions, averages, color='skyblue')

# Adding value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

plt.xticks(rotation=45, ha="right")  # Rotate labels to improve readability
plt.xlabel('Question Topics', fontsize=14)
plt.ylabel('Average Score', fontsize=14)
plt.title('Application Usability Feedback', fontsize=16)
plt.ylim(0, 5.5)  # Set the limits to match the 1-5 scale of the averages
plt.axhline(y=1, color='r', linestyle='--')
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.show()