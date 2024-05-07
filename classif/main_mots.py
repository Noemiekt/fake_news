import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Data preparation
data = {
    "Word": [
        "musk", "humain", "neuralink", "certains", "projet", "puce", "pensée", "ordinateur", "pourquoi", "souris",
        "elon", "avec", "technologie", "nouveau", "neurons", "poura", "pour", "neurones", "podcast", "peuvent",
        "patient", "passer", "oreilles", "neuroscience", "neuron", "news", "notre", "nouvelle", "aide", "premier"
    ],
    "Mean_TFIDF_Score": [
        0.181902, 0.181902, 0.121268, 0.121268, 0.121268, 0.121268, 0.121268, 0.121268, 0.121268, 0.121268,
        0.121268, 0.121268, 0.121268, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634,
        0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634, 0.060634
    ]
}
df = pd.DataFrame(data)

# Generate a horizontal bar chart
plt.figure(figsize=(10, 10))  # Adjust figure size to fit all labels comfortably
plt.barh(df['Word'], df['Mean_TFIDF_Score'], color='dodgerblue')
plt.xlabel('Mean TFIDF Score')
plt.ylabel('Words')
plt.title('TFIDF Scores by Word')
plt.gca().invert_yaxis()  # Optionally invert y-axis so the largest values are on top

plt.tight_layout()
plt.show()

# Specify the path to a TrueType font
font_path = 'font.ttf'  # Update this to the path of a TrueType font available on your system

# Generate a word cloud using the specified TrueType font
wc = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    max_words=100, 
    font_path=font_path  # Specify the font path here
).generate_from_frequencies(dict(zip(df['Word'], df['Mean_TFIDF_Score'])))

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('TFIDF Word Cloud')
plt.show()