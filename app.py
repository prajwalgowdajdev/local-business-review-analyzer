import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go

st.set_page_config(
    page_title="LBR Insight Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background: #F4F7FB; }
.block-container { max-width: 1400px; padding-top: 1.5rem; padding-bottom: 3rem; }

.brand {
    color: #1D4ED8;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.hero {
    color: #0F172A;
    font-size: 42px;
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-sub {
    color: #64748B;
    font-size: 16px;
    margin-bottom: 28px;
}

.section-title {
    color: #0F172A;
    font-size: 25px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 18px;
}

.input-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 22px;
    min-height: 130px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.kpi-label {
    color: #64748B;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.kpi-number {
    color: #0F172A;
    font-size: 34px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-caption {
    color: #94A3B8;
    font-size: 13px;
    margin-top: 3px;
}

.pulse-card {
    background: #0F172A;
    border-radius: 18px;
    padding: 25px;
    color: white;
    min-height: 130px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.12);
}

.pulse-label {
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.pulse-number {
    color: white;
    font-size: 46px;
    font-weight: 800;
    margin-top: 5px;
}

.pulse-caption {
    color: #94A3B8;
    font-size: 13px;
}

.topic-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
}

.topic-number {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.topic-name {
    color: #0F172A;
    font-size: 19px;
    font-weight: 800;
    margin-top: 4px;
}

.topic-detail {
    color: #64748B;
    font-size: 13px;
    margin-top: 5px;
}

.action-card {
    background: #0F172A;
    border-radius: 16px;
    padding: 21px;
    color: white;
    margin-bottom: 12px;
}

.action-label {
    color: #93C5FD;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.action-title {
    color: white;
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.action-text {
    color: #CBD5E1;
    font-size: 13px;
    margin-top: 7px;
}

.info-bar {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 14px 18px;
    color: #1E3A8A;
    font-size: 13px;
}

.stButton > button {
    background: #1D4ED8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-weight: 700;
    font-size: 15px;
}

.stButton > button:hover {
    background: #1E40AF;
    color: white;
}

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# Download VADER lexicon automatically when running on Streamlit Cloud
try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download("vader_lexicon", quiet=True)
    sia = SentimentIntensityAnalyzer()


business_keywords = [
    "food", "taste", "tasty", "delicious", "meal", "restaurant", "cafe",
    "hotel", "service", "staff", "waiter", "employee", "price", "prices",
    "expensive", "cheap", "cost", "quality", "portion", "clean",
    "cleanliness", "dirty", "hygiene", "parking", "atmosphere", "ambience",
    "environment", "delivery", "order", "ordered", "menu", "customer",
    "experience", "wait", "waiting", "slow", "fast", "friendly", "helpful",
    "comfortable"
]


def is_business_review(text):
    text_lower = text.lower()
    return any(
        keyword in text_lower
        for keyword in business_keywords
    )


topics = {
    "Food": [
        "food", "taste", "tasty", "delicious", "biryani",
        "meal", "fresh", "quality", "portion"
    ],
    "Service": [
        "service", "served", "serving", "customer service"
    ],
    "Staff": [
        "staff", "employee", "waiter", "workers",
        "friendly", "helpful"
    ],
    "Price": [
        "price", "prices", "expensive", "cheap",
        "cost", "value", "portion"
    ],
    "Cleanliness": [
        "clean", "cleanliness", "dirty", "hygiene"
    ],
    "Parking": [
        "parking", "park", "car"
    ],
    "Atmosphere": [
        "atmosphere", "ambience", "environment",
        "beautiful", "comfortable"
    ],
    "Waiting Time": [
        "waiting", "waited", "wait", "slow",
        "minutes", "time"
    ]
}


st.html("""
<div class="brand">LBR / INSIGHT ENGINE</div>
<div class="hero">Local Business Review Intelligence</div>
<div class="hero-sub">
    Turn customer feedback into clear business insights and actionable decisions.
</div>
""")


st.html("""
<div class="section-title">Analyze Customer Feedback</div>
<div class="section-subtitle">
    Enter a business and paste customer reviews to generate an instant insight report.
</div>
""")


business_name = st.text_input(
    "Business Name",
    placeholder="Example: Urban Bites Restaurant"
)


reviews = st.text_area(
    "Customer Reviews",
    height=190,
    placeholder="Paste customer reviews here...\n\nUse one review per line."
)


st.write("")


analyze = st.button(
    "✦  ANALYZE CUSTOMER PULSE",
    type="primary",
    use_container_width=True
)


if analyze:

    if not business_name.strip():
        st.warning("Please enter a business name.")

    elif not reviews.strip():
        st.warning("Please paste some customer reviews.")

    else:

        review_list = [
            review.strip()
            for review in reviews.split("\n")
            if review.strip()
        ]

        invalid_reviews = [
            review
            for review in review_list
            if not is_business_review(review)
        ]

        if invalid_reviews:

            st.warning(
                "Some input does not appear to be a business review."
            )

            st.html("""
            <div class="info-bar">
                Please enter feedback related to food, service,
                staff, price, cleanliness, parking, delivery,
                waiting time, or the overall customer experience.
            </div>
            """)

            st.caption(
                f'Unrecognized input: "{invalid_reviews[0]}"'
            )

            st.stop()


        positive = 0
        neutral = 0
        negative = 0

        results = []


        for review in review_list:

            score = sia.polarity_scores(review)["compound"]

            if score >= 0.05:
                sentiment = "Positive"
                positive += 1

            elif score <= -0.05:
                sentiment = "Negative"
                negative += 1

            else:
                sentiment = "Neutral"
                neutral += 1

            results.append({
                "review": review,
                "sentiment": sentiment,
                "score": score
            })


        total = len(review_list)

        positive_pct = round(
            (positive / total) * 100
        )

        neutral_pct = round(
            (neutral / total) * 100
        )

        negative_pct = round(
            (negative / total) * 100
        )


        topic_data = {}

        for topic in topics:

            topic_data[topic] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "reviews": []
            }


        for item in results:

            text = item["review"].lower()

            for topic, keywords in topics.items():

                matched = any(
                    keyword in text
                    for keyword in keywords
                )

                if matched:

                    sentiment_key = item["sentiment"].lower()

                    topic_data[topic][sentiment_key] += 1

                    topic_data[topic]["reviews"].append(item)


        st.divider()


        st.html(f"""
        <div class="section-title">{business_name}</div>
        <div class="section-subtitle">
            Customer intelligence generated from {total} review(s)
        </div>
        """)


        st.html("""
        <div class="section-title">Customer Pulse</div>
        """)


        c1, c2, c3, c4 = st.columns(
            [1.2, 1, 1, 1]
        )


        with c1:

            pulse_score = positive_pct - negative_pct

            st.html(f"""
            <div class="pulse-card">
                <div class="pulse-label">CUSTOMER SENTIMENT</div>
                <div class="pulse-number">{pulse_score:+d}</div>
                <div class="pulse-caption">
                    Positive vs. negative balance
                </div>
            </div>
            """)


        with c2:

            st.html(f"""
            <div class="kpi-card">
                <div class="kpi-label">Positive</div>
                <div class="kpi-number">{positive_pct}%</div>
                <div class="kpi-caption">{positive} review(s)</div>
            </div>
            """)


        with c3:

            st.html(f"""
            <div class="kpi-card">
                <div class="kpi-label">Neutral</div>
                <div class="kpi-number">{neutral_pct}%</div>
                <div class="kpi-caption">{neutral} review(s)</div>
            </div>
            """)


        with c4:

            st.html(f"""
            <div class="kpi-card">
                <div class="kpi-label">Negative</div>
                <div class="kpi-number">{negative_pct}%</div>
                <div class="kpi-caption">{negative} review(s)</div>
            </div>
            """)


        st.html("""
        <div class="section-title">Sentiment Distribution</div>
        """)


        st.progress(
            positive_pct / 100
        )


        st.caption(
            f"Positive: {positive_pct}%   •   "
            f"Neutral: {neutral_pct}%   •   "
            f"Negative: {negative_pct}%"
        )


        positive_topics = []
        negative_topics = []


        for topic, data in topic_data.items():

            mentions = (
                data["positive"]
                + data["negative"]
                + data["neutral"]
            )

            if mentions > 0:

                positive_topics.append(
                    (
                        topic,
                        data["positive"],
                        mentions
                    )
                )

                negative_topics.append(
                    (
                        topic,
                        data["negative"],
                        mentions
                    )
                )


        positive_topics.sort(
            key=lambda x: x[1],
            reverse=True
        )

        negative_topics.sort(
            key=lambda x: x[1],
            reverse=True
        )


        st.divider()


        st.html("""
        <div class="section-title">Business Priorities</div>
        <div class="section-subtitle">
            Key themes detected from customer feedback.
        </div>
        """)


        left, right = st.columns(2)


        with left:

            st.markdown("### ✦ Top Positive Trends")

            top_positive = [
                item
                for item in positive_topics
                if item[1] > 0
            ][:3]


            if top_positive:

                for index, (
                    topic,
                    count,
                    mentions
                ) in enumerate(
                    top_positive,
                    start=1
                ):

                    st.html(f"""
                    <div class="topic-card">
                        <div class="topic-number">
                            STRENGTH {index:02d}
                        </div>

                        <div class="topic-name">
                            {topic}
                        </div>

                        <div class="topic-detail">
                            {count} positive signal(s)
                            across {mentions} mention(s)
                        </div>
                    </div>
                    """)

            else:

                st.info(
                    "No clear positive trends detected."
                )


        with right:

            st.markdown("### ⚠ Top Negative Issues")

            top_negative = [
                item
                for item in negative_topics
                if item[1] > 0
            ][:3]


            if top_negative:

                for index, (
                    topic,
                    count,
                    mentions
                ) in enumerate(
                    top_negative,
                    start=1
                ):

                    st.html(f"""
                    <div class="topic-card">
                        <div class="topic-number">
                            ISSUE {index:02d}
                        </div>

                        <div class="topic-name">
                            {topic}
                        </div>

                        <div class="topic-detail">
                            {count} negative signal(s)
                            across {mentions} mention(s)
                        </div>
                    </div>
                    """)

            else:

                st.info(
                    "No major negative issues detected."
                )


        st.divider()


        st.html("""
        <div class="section-title">Review Intelligence Map</div>
        <div class="section-subtitle">
            Positive and negative signals across business topics.
        </div>
        """)


        chart_topics = []
        positive_counts = []
        negative_counts = []


        for topic, data in topic_data.items():

            mentions = (
                data["positive"]
                + data["negative"]
                + data["neutral"]
            )

            if mentions > 0:

                chart_topics.append(topic)

                positive_counts.append(
                    data["positive"]
                )

                negative_counts.append(
                    data["negative"]
                )


        if chart_topics:

            fig = go.Figure()


            fig.add_trace(
                go.Bar(
                    name="Positive",
                    x=chart_topics,
                    y=positive_counts
                )
            )


            fig.add_trace(
                go.Bar(
                    name="Negative",
                    x=chart_topics,
                    y=negative_counts
                )
            )


            fig.update_layout(
                barmode="group",
                height=430,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=80
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                font=dict(
                    color="#0F172A"
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis=dict(
                    title="Business Topic"
                ),
                yaxis=dict(
                    title="Review Signals",
                    dtick=1
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough topic information to create the chart."
            )


        st.divider()


        st.html("""
        <div class="section-title">AI Strategist</div>
        <div class="section-subtitle">
            Suggested actions based on detected customer issues.
        </div>
        """)


        advice = []


        for topic, count, mentions in top_negative:

            if topic == "Waiting Time":

                advice.append(
                    (
                        "Reduce waiting time",
                        "Review peak-hour staffing and kitchen workflow to reduce delays."
                    )
                )

            elif topic == "Parking":

                advice.append(
                    (
                        "Improve parking guidance",
                        "Provide clearer parking information and available alternatives."
                    )
                )

            elif topic == "Price":

                advice.append(
                    (
                        "Improve perceived value",
                        "Review pricing, portion sizes and value communication."
                    )
                )

            elif topic == "Service":

                advice.append(
                    (
                        "Strengthen service consistency",
                        "Monitor service speed during busy periods and standardize the process."
                    )
                )

            elif topic == "Staff":

                advice.append(
                    (
                        "Continue staff development",
                        "Maintain staff training and reinforce positive customer interactions."
                    )
                )

            elif topic == "Food":

                advice.append(
                    (
                        "Protect food quality",
                        "Maintain consistency in taste, freshness and portion quality."
                    )
                )

            elif topic == "Cleanliness":

                advice.append(
                    (
                        "Maintain cleanliness",
                        "Use regular cleaning checks throughout operating hours."
                    )
                )

            elif topic == "Atmosphere":

                advice.append(
                    (
                        "Preserve the atmosphere",
                        "Continue maintaining the environment customers appreciate."
                    )
                )


        if advice:

            for index, (
                title,
                description
            ) in enumerate(
                advice[:3],
                start=1
            ):

                st.html(f"""
                <div class="action-card">

                    <div class="action-label">
                        ACTION {index:02d}
                    </div>

                    <div class="action-title">
                        {title}
                    </div>

                    <div class="action-text">
                        {description}
                    </div>

                </div>
                """)

        else:

            st.success(
                "No major negative patterns detected. "
                "Continue monitoring customer feedback."
            )


st.html("""
<div class="footer">
    LBR Insight Engine · Local Business Review Intelligence
</div>
""")