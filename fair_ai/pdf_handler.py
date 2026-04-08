# PDF से text निकालना + dataset बनाने की कोशिश

import PyPDF2
import pandas as pd


# -------------------------------
# Extract text
# -------------------------------
def extract_text_from_pdf(file):
    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


# -------------------------------
# Convert text to dataframe (basic AI logic)
# -------------------------------
def text_to_dataframe(text):
    """
    simple heuristic:
    comma या space separated data detect करेगा
    """

    lines = text.strip().split("\n")

    data = []

    for line in lines:
        # अगर line meaningful है
        if len(line.split()) > 2:
            # try comma split
            if "," in line:
                row = line.split(",")
            else:
                row = line.split()

            data.append(row)

    # dataframe बनाने की कोशिश
    try:
        df = pd.DataFrame(data)

        # first row को header मान लो
        df.columns = df.iloc[0]
        df = df[1:]

        return df

    except:
        return None