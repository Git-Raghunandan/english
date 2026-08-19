import json
import random
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kids English Learning",
    page_icon="📚",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        max-width: 750px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 21px;
        margin-bottom: 25px;
    }

    .word-card {
        padding: 30px;
        border-radius: 25px;
        border: 3px solid #dddddd;
        text-align: center;
        margin: 20px 0;
    }

    .big-word {
        font-size: 55px;
        font-weight: bold;
    }

    .meaning {
        font-size: 25px;
        margin-top: 10px;
    }

    .sentence {
        font-size: 24px;
        margin-top: 15px;
    }

    .emoji {
        font-size: 70px;
    }

    .question {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin: 25px 0;
    }

    .score {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
    }

    .trophy {
        text-align: center;
        font-size: 120px;
    }

    @media (max-width: 600px) {

        .title {
            font-size: 32px;
        }

        .subtitle {
            font-size: 18px;
        }

        .big-word {
            font-size: 45px;
        }

        .meaning {
            font-size: 21px;
        }

        .sentence {
            font-size: 20px;
        }

        .question {
            font-size: 23px;
        }

        .trophy {
            font-size: 90px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD QUESTIONS FILE
# ============================================================

QUESTION_FILE = (
    Path(__file__).parent
    / "Questions"
    / "english_questions.json"
)


def load_questions():

    if not QUESTION_FILE.exists():

        st.error(
            "❌ English question file not found."
        )

        st.info(
            "Please create: "
            "Questions/english_questions.json"
        )

        st.stop()

    try:

        with open(
            QUESTION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        st.error(
            "❌ The JSON file contains an error."
        )

        st.code(str(error))

        st.stop()

    except Exception as error:

        st.error(
            "❌ Could not read the question file."
        )

        st.code(str(error))

        st.stop()

    return data


# ============================================================
# QUESTION BANK
# ============================================================

QUESTION_BANK = load_questions()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {

    "mode": None,

    "learn_index": 0,

    "quiz_questions": [],

    "quiz_index": 0,

    "score": 0,

    "answered": False,

    "last_result": None,

    "student_name": ""

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# RESET QUIZ
# ============================================================

def reset_quiz():

    st.session_state.mode = None

    st.session_state.quiz_questions = []

    st.session_state.quiz_index = 0

    st.session_state.score = 0

    st.session_state.answered = False

    st.session_state.last_result = None


# ============================================================
# CREATE RANDOM QUIZ
# ============================================================

def create_quiz(number):

    number = min(
        number,
        len(QUESTION_BANK)
    )

    # random.sample prevents duplicate questions
    questions = random.sample(
        QUESTION_BANK,
        number
    )

    # Shuffle options
    quiz = []

    for item in questions:

        question = item.copy()

        question["options"] = (
            item["options"].copy()
        )

        random.shuffle(
            question["options"]
        )

        quiz.append(question)

    return quiz


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.mode is None:

    st.markdown(
        '<div class="title">'
        '📚 Learn English!'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Fun English for Kids 🌟 By Swarup'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    name = st.text_input(
        "👧 Child's Name",
        placeholder="Enter your name"
    )


    st.write("")


    # --------------------------------------------------------
    # LEARNING MODES
    # --------------------------------------------------------

    st.subheader(
        "What would you like to do?"
    )


    if st.button(
        "🧠 LEARN WORDS",
        use_container_width=True
    ):

        st.session_state.student_name = (
            name.strip()
            if name.strip()
            else "Little Learner"
        )

        st.session_state.mode = "learn"

        st.session_state.learn_index = 0

        st.rerun()


    st.write("")


    if st.button(
        "✏️ WORD QUIZ",
        use_container_width=True
    ):

        st.session_state.student_name = (
            name.strip()
            if name.strip()
            else "Little Learner"
        )

        st.session_state.quiz_questions = create_quiz(
            10
        )

        st.session_state.quiz_index = 0

        st.session_state.score = 0

        st.session_state.answered = False

        st.session_state.last_result = None

        st.session_state.mode = "word_quiz"

        st.rerun()


    st.write("")


    if st.button(
        "💬 SENTENCE QUIZ",
        use_container_width=True
    ):

        st.session_state.student_name = (
            name.strip()
            if name.strip()
            else "Little Learner"
        )

        st.session_state.quiz_questions = create_quiz(
            10
        )

        st.session_state.quiz_index = 0

        st.session_state.score = 0

        st.session_state.answered = False

        st.session_state.last_result = None

        st.session_state.mode = "sentence_quiz"

        st.rerun()


# ============================================================
# LEARN WORDS
# ============================================================

elif st.session_state.mode == "learn":

    index = st.session_state.learn_index

    word_data = QUESTION_BANK[index]


    st.markdown(
        '<div class="title">'
        '🧠 Learn New Words'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        f"Hello "
        f"**{st.session_state.student_name}**! 👋"
    )


    st.progress(
        (index + 1) / len(QUESTION_BANK)
    )


    # --------------------------------------------------------
    # WORD CARD
    # --------------------------------------------------------

    st.markdown(
        '<div class="word-card">',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="emoji">'
        f'{word_data["emoji"]}'
        f'</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="big-word">'
        f'{word_data["word"]}'
        f'</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="meaning">'
        f'📖 {word_data["meaning"]}'
        f'</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="sentence">'
        f'💬 "{word_data["sentence"]}"'
        f'</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    st.write("")


    # --------------------------------------------------------
    # NEXT WORD
    # --------------------------------------------------------

    if index < len(QUESTION_BANK) - 1:

        if st.button(
            "➡️ NEXT WORD",
            use_container_width=True
        ):

            st.session_state.learn_index += 1

            st.rerun()

    else:

        st.success(
            "🎉 You learned all the words!"
        )


        if st.button(
            "🏠 BACK TO HOME",
            use_container_width=True
        ):

            reset_quiz()

            st.rerun()


# ============================================================
# QUIZ
# ============================================================

else:

    questions = st.session_state.quiz_questions

    index = st.session_state.quiz_index

    total = len(questions)


    # ========================================================
    # QUIZ COMPLETE
    # ========================================================

    if index >= total:

        score = st.session_state.score


        percentage = int(
            score / total * 100
        )


        if score == total:

            st.balloons()

            st.snow()


            st.markdown(
                '<div class="trophy">'
                '🏆'
                '</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                '<div class="title">'
                '🎉 PERFECT SCORE! 🎉'
                '</div>',
                unsafe_allow_html=True
            )


            st.success(
                f"Fantastic, "
                f"{st.session_state.student_name}!"
            )


            st.markdown(
                f'<div class="score">'
                f'{score} / {total}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:35px;
                ">
                    💯 100% 💯
                    <br><br>
                    ⭐ ⭐ ⭐ ⭐ ⭐
                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            st.markdown(
                '<div class="title">'
                '🎉 Quiz Complete!'
                '</div>',
                unsafe_allow_html=True
            )


            st.success(
                f"Good job, "
                f"{st.session_state.student_name}! 🌟"
            )


            st.markdown(
                f'<div class="score">'
                f'{score} / {total}'
                f'</div>',
                unsafe_allow_html=True
            )


            st.write(
                f"Your score is "
                f"**{percentage}%**"
            )


            if percentage >= 80:

                st.info(
                    "🌟 Excellent work!"
                )

            elif percentage >= 60:

                st.info(
                    "👍 Good job! Keep practicing!"
                )

            else:

                st.warning(
                    "💪 Keep practicing. You can do it!"
                )


        st.write("")


        if st.button(
            "🏠 BACK TO HOME",
            use_container_width=True
        ):

            reset_quiz()

            st.rerun()


    # ========================================================
    # CURRENT QUESTION
    # ========================================================

    else:

        data = questions[index]


        st.markdown(
            '<div class="title">'
            '✏️ English Quiz'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            f"👧 **{st.session_state.student_name}**"
        )


        st.progress(
            (index + 1) / total
        )


        st.write(
            f"Question **{index + 1}** "
            f"of **{total}**"
        )


        # ====================================================
        # WORD QUIZ
        # ====================================================

        if st.session_state.mode == "word_quiz":

            st.markdown(
                f'<div class="question">'
                f'Which word means: '
                f'<br><br>'
                f'📖 {data["meaning"]}'
                f'</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # SENTENCE QUIZ
        # ====================================================

        else:

            st.markdown(
                f'<div class="question">'
                f'Which sentence uses '
                f'<b>{data["word"]}</b> correctly?'
                f'</div>',
                unsafe_allow_html=True
            )


        # ====================================================
        # ANSWERS
        # ====================================================

        if not st.session_state.answered:

            selected = st.radio(
                "Choose your answer:",
                data["options"],
                key=f"answer_{index}"
            )


            st.write("")


            if st.button(
                "✅ CHECK ANSWER",
                use_container_width=True
            ):

                if selected == data["answer"]:

                    st.session_state.score += 1

                    st.session_state.last_result = (
                        "correct"
                    )

                else:

                    st.session_state.last_result = (
                        "wrong"
                    )


                st.session_state.answered = True

                st.rerun()


        # ====================================================
        # RESULT
        # ====================================================

        else:

            if (
                st.session_state.last_result
                == "correct"
            ):

                st.success(
                    "🎉 CORRECT! Great job!"
                )

            else:

                st.error(
                    "❌ Not quite!"
                )


                st.write(
                    f"The correct answer is:"
                )


                st.info(
                    data["answer"]
                )


            st.write("")


            if st.button(
                "➡️ NEXT QUESTION",
                use_container_width=True
            ):

                st.session_state.quiz_index += 1

                st.session_state.answered = False

                st.session_state.last_result = None

                st.rerun()
