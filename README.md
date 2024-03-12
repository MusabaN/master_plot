# Data Structure in `resultater23.tsv`

The data file `resultater23.tsv` is structured as follows:

- **First Row**: Contains the column headers, which include `test_subject`, `tid` (the time it took for the test subject to complete the test), and various multiple choice questions. Each question is represented in its own column. If it ends with _proc, it is for the questions about processes, if it ends with _virt it is the questions about virtual memory. And if it doesnt end in either, it is a general question not related to the subject.

- **First Column**: Contains the row headers. The first 3 column headers are questions, answers and correct_answers, the rest are integers from 0-48 which is the test_subject_id for the different answers

- **Second Row**: Contains the questions for the multiple choice.

- **Third Row**: Provides the different answer options for each question, comma-separated within each column. This row is used to list the available answers that test subjects could choose from for each multiple-choice question.

- **Fourth Row**: Lists the correct answers for the multiple-choice questions that have a definitive correct answer. Questions that do not have a correct answer (e.g., opinion-based questions) are filled with a dash ('-'). Similarly, the `test_subject` and `tid` columns are filled with dashes in this row, indicating that this row does not pertain to actual test subject data.

- **Fifth Row Onwards**: Contains the responses from the test subjects. Each row represents a single test subject's answers to the survey, including their ID, the time it took them to complete the survey (`tid`), and their selected answers for each question. Answers are comma-separated, matching the format provided in the second row.

## Scoring Logic

- All questions with correct answers, have only one correct answer.
- If a test subject chooses multiple answers, they get 0 points
- If a test subject selects only one answer and it is wrong, they receive 0 points for that question.
- If a test subject chooses the correct answer (and only that answer) for questions with a correct answer, they are awarded 1 point for that question.

The entire file is tab-separated, with columns clearly delineated by tabulator spaces between each piece of data.