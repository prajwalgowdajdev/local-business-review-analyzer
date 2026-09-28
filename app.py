import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="LBR Insight Engine",
    page_icon="◈",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #F5F7FB;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Brand */

.brand {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #6366F1;
}

/* Hero */

.hero {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    margin-top: 5px;
    margin-bottom: 5px;
}

.hero-sub {
    color: #6B7280;
    font-size: 16px;
    margin-bottom: 30px;
}

/* General card */

.card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.035);
}

.card-title {
    font-size: 13px;
    font-weight: 700;
    color: #6B7280;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.big-number {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
    margin-top: 8px;
}

.small-text {
    color: #6B7280;
    font-size: 13px;
}

/* Customer pulse */

.pulse-card {
    background: #111827;
    border-radius: 20px;
    padding: 28px;
    color: white;
}

.pulse-title {
    font-size: 14px;
    letter-spacing: 1px;
    font-weight: 700;
    color: #CBD5E1;
}

.pulse-number {
    font-size: 52px;
    font-weight: 800;
    margin-top: 8px;
}

.pulse-description {
    color: #CBD5E1;
    font-size: 14px;
}

/* Topic cards */

.topic-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}

.topic-number {
    font-size: 12px;
    font-weight: 700;
    color: #9CA3AF;
    letter-spacing: 1px;
}

.topic-name {
    font-size: 20px;
    font-weight: 800;
    color: #111827;
    margin-top: 5px;
}

.topic-detail {
    color: #6B7280;
    font-size: 13px;
    margin-top: 5px;
}

/* AI action cards */

.priority-card {
    background: #111827;
    border-radius: 18px;
    padding: 24px;
    color: white;
    margin-bottom: 12px;
}

.priority-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #A5B4FC;
}

.priority-title {
    font-size: 20px;
    font-weight: 800;
    margin-top: 6px;
}

.priority-text {
    color: #CBD5E1;
    font-size: 14px;
    margin-top: 8px;
}

/* Footer */

.footer {
    text-align: center;
    color: #9CA3AF;
    font-size: 12px;
    margin-top: 60px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SENTIMENT ANALYZER
# ---------------------------------------------------------

sia = SentimentIntensityAnalyzer()


# ---------------------------------------------------------
# BUSINESS TOPICS
# ---------------------------------------------------------

topics = {

    "Food": [
        "food",
        "taste",
        "tasty",
        "delicious",
        "biryani",
        "meal",
        "fresh",
        "quality",
        "portion"
    ],

    "Service": [
        "service",
        "served",
        "serving",
        "customer service"
    ],

    "Staff": [
        "staff",
        "employee",
        "waiter",
        "workers",
        "friendly",
        "helpful"
    ],

    "Price": [
        "price",
        "prices",
        "expensive",
        "cheap",
        "cost",
        "value",
        "portion"
    ],

    "Cleanliness": [
        "clean",
        "cleanliness",
        "dirty",
        "hygiene"
    ],

    "Parking": [
        "parking",
        "park",
        "car"
    ],

    "Atmosphere": [
        "atmosphere",
        "ambience",
        "environment",
        "beautiful",
        "comfortable"
    ],

    "Waiting Time": [
        "waiting",
        "waited",
        "wait",
        "slow",
        "minutes",
        "time"
    ]
}


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.html("""
<div class="brand">
    LBR / INSIGHT ENGINE
</div>

<div class="hero">
    Understand what your customers really mean.
</div>

<div class="hero-sub">
    AI-powered review intelligence for local businesses.
</div>
""")


# ---------------------------------------------------------
# BUSINESS INPUT
# ---------------------------------------------------------

st.markdown("### Business")

business_name = st.text_input(
    "Business",
    placeholder="e.g. Urban Bites Restaurant",
    label_visibility="collapsed"
)


# ---------------------------------------------------------
# REVIEW INPUT
# ---------------------------------------------------------

st.markdown("### Customer Reviews")

reviews = st.text_area(
    "Reviews",
    height=220,
    placeholder=(
        "Paste your Google or Yelp reviews here...\n\n"
        "One review per line."
    ),
    label_visibility="collapsed"
)

st.write("")


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

analyze = st.button(
    "✦  ANALYZE CUSTOMER PULSE",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if analyze:

    # Check business name

    if not business_name.strip():

        st.warning("Enter a business name.")

    # Check reviews

    elif not reviews.strip():

        st.warning("Paste some customer reviews.")

    else:

        # -------------------------------------------------
        # SPLIT REVIEWS
        # -------------------------------------------------

        review_list = [
            review.strip()
            for review in reviews.split("\n")
            if review.strip()
        ]


        # -------------------------------------------------
        # SENTIMENT COUNTS
        # -------------------------------------------------

        positive = 0
        neutral = 0
        negative = 0

        results = []


        # -------------------------------------------------
        # SENTIMENT ANALYSIS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # PERCENTAGES
        # -------------------------------------------------

        total = len(review_list)

        positive_pct = round((positive / total) * 100)
        neutral_pct = round((neutral / total) * 100)
        negative_pct = round((negative / total) * 100)


        # -------------------------------------------------
        # TOPIC DATA
        # -------------------------------------------------

        topic_data = {}

        for topic in topics:

            topic_data[topic] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0,
                "reviews": []
            }


        # -------------------------------------------------
        # MATCH REVIEWS TO TOPICS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # BUSINESS HEADER
        # -------------------------------------------------

        st.divider()

        st.markdown(f"## {business_name}")

        st.caption(
            f"Customer intelligence generated from {total} reviews"
        )


        # =================================================
        # CUSTOMER PULSE
        # =================================================

        st.markdown("### Customer Pulse")

        c1, c2 = st.columns([1, 2])


        # -------------------------------------------------
        # PULSE SCORE
        # -------------------------------------------------

        with c1:

            pulse_score = positive_pct - negative_pct

            st.html(f"""
            <div class="pulse-card">

                <div class="pulse-title">
                    CUSTOMER SENTIMENT
                </div>

                <div class="pulse-number">
                    {pulse_score:+d}
                </div>

                <div class="pulse-description">
                    Positive vs. negative sentiment balance
                </div>

            </div>
            """)


        # -------------------------------------------------
        # SENTIMENT CARDS
        # -------------------------------------------------

        with c2:

            a, b, c = st.columns(3)


            # Positive

            with a:

                st.html(f"""
                <div class="card">

                    <div class="card-title">
                        Positive
                    </div>

                    <div class="big-number">
                        {positive_pct}%
                    </div>

                    <div class="small-text">
                        {positive} reviews
                    </div>

                </div>
                """)


            # Neutral

            with b:

                st.html(f"""
                <div class="card">

                    <div class="card-title">
                        Neutral
                    </div>

                    <div class="big-number">
                        {neutral_pct}%
                    </div>

                    <div class="small-text">
                        {neutral} reviews
                    </div>

                </div>
                """)


            # Negative

            with c:

                st.html(f"""
                <div class="card">

                    <div class="card-title">
                        Negative
                    </div>

                    <div class="big-number">
                        {negative_pct}%
                    </div>

                    <div class="small-text">
                        {negative} reviews
                    </div>

                </div>
                """)


        # =================================================
        # SENTIMENT DISTRIBUTION
        # =================================================

        st.markdown("### Sentiment Distribution")

        st.progress(positive_pct / 100)

        st.caption(
            f"{positive_pct}% positive  •  "
            f"{neutral_pct}% neutral  •  "
            f"{negative_pct}% negative"
        )


        # =================================================
        # TOPIC ANALYSIS
        # =================================================

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


        # Sort topics

        positive_topics.sort(
            key=lambda x: x[1],
            reverse=True
        )

        negative_topics.sort(
            key=lambda x: x[1],
            reverse=True
        )


        # =================================================
        # BUSINESS PRIORITIES
        # =================================================

        st.divider()

        st.markdown("## Business Priorities")

        st.caption(
            "The strongest themes detected in customer feedback."
        )


        # =================================================
        # TOP POSITIVE TRENDS
        # =================================================

        st.markdown("### ✦ Top 3 Positive Trends")


        top_positive = [
            item
            for item in positive_topics
            if item[1] > 0
        ][:3]


        if top_positive:

            for index, (topic, count, mentions) in enumerate(
                top_positive,
                start=1
            ):

                st.html(f"""
                <div class="topic-card">

                    <div class="topic-number">
                        PRIORITY {index:02d}
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


        # =================================================
        # TOP NEGATIVE ISSUES
        # =================================================

        st.markdown("### ⚠ Top 3 Negative Issues")


        top_negative = [
            item
            for item in negative_topics
            if item[1] > 0
        ][:3]


        if top_negative:

            for index, (topic, count, mentions) in enumerate(
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


        # =================================================
        # REVIEW INTELLIGENCE MAP
        # =================================================

        st.divider()

        st.markdown("## Review Intelligence Map")

        st.caption(
            "Positive and negative signals by business topic."
        )


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


        # -------------------------------------------------
        # CHART
        # -------------------------------------------------

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

                height=420,

                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                ),

                paper_bgcolor="white",

                plot_bgcolor="white",

                font=dict(
                    color="#111827"
                ),

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
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


        # =================================================
        # AI STRATEGIST
        # =================================================

        st.divider()

        st.markdown("## AI Strategist")

        st.caption(
            "Recommended actions based on detected customer issues."
        )


        advice = []


        # -------------------------------------------------
        # GENERATE BUSINESS ADVICE
        # -------------------------------------------------

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


        # -------------------------------------------------
        # DISPLAY ADVICE
        # -------------------------------------------------

        if advice:

            for index, (title, description) in enumerate(
                advice[:3],
                start=1
            ):

                st.html(f"""
                <div class="priority-card">

                    <div class="priority-label">
                        ACTION {index:02d}
                    </div>

                    <div class="priority-title">
                        {title}
                    </div>

                    <div class="priority-text">
                        {description}
                    </div>

                </div>
                """)

        else:

            st.success(
                "No major negative patterns detected. "
                "Continue monitoring customer feedback."
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.html("""
<div class="footer">
    LBR Insight Engine • Local Business Review Intelligence
</div>
""")