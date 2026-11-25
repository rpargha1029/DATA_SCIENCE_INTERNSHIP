"""Month 3 Bonus Deliverable: Generate 5-Slide Business vs. Entertainment Comparison Deck."""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PPTX = BASE_DIR / "Business_vs_Entertainment_Comparison_Deck.pptx"


def add_bullet_slide(prs: Presentation, title: str, bullets: list[str]) -> None:
    """Add a title-and-content slide with clean bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    tf = slide.placeholders[1].text_frame
    tf.clear()
    for idx, text in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = text
        p.font.size = Pt(18)
        p.space_after = Pt(10)


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = "Month 3 EDA Comparison: Business Data vs. Entertainment Data"
    title_slide.placeholders[1].text = (
        "Task 3 (Telecom Customer Churn) vs. Task 4 (Netflix Titles)\n"
        "Data Science Internship Portfolio"
    )

    # Slide 2: Dataset Structure & Cleaning Challenges
    add_bullet_slide(
        prs,
        "1. Dataset Structure & Cleaning Challenges",
        [
            "Business (Telco Churn): ~7,000 structured customer billing & service rows; hidden whitespace (' ') in numeric TotalCharges.",
            "Entertainment (Netflix): ~9,000 semi-structured media metadata rows; multi-label strings (cast, country, listed_in) & date parsing.",
            "Key Lesson: Numeric coercion & blank-string checks are critical in business data, while string splitting & explode() are vital in media metadata.",
        ],
    )

    # Slide 3: Feature Engineering Strategies
    add_bullet_slide(
        prs,
        "2. Feature Engineering Approaches",
        [
            "Business (Telco Churn): Domain-driven ratios (AvgMonthlySpend = TotalCharges / tenure), tenure buckets, binary & one-hot encoding.",
            "Entertainment (Netflix): Temporal extraction (release_decade, datetime date_added), content_type flags (is_movie), primary country parsing.",
            "Key Lesson: Feature engineering aligns directly with the analytical goal—retention risk vs. catalog strategy.",
        ],
    )

    # Slide 4: Visual Storytelling & Analytical Insights
    add_bullet_slide(
        prs,
        "3. Visual Storytelling & Core Insights",
        [
            "Telco Churn: Countplots, contract-vs-churn barplots, boxplots, and correlation heatmaps isolate high-risk month-to-month segments.",
            "Netflix EDA: Pie charts, release-year line plots, top-10 genre barplots, country heatmaps, and a 2-year trend forecast.",
            "Key Lesson: Business EDA prioritizes driver attribution; Entertainment EDA highlights temporal growth and regional diversity.",
        ],
    )

    # Slide 5: Strategic Takeaways & Modeling Readiness
    add_bullet_slide(
        prs,
        "4. Strategic Takeaways & Next Steps",
        [
            "Telco Churn output is ML-ready (cleaned numeric + encoded CSV) for binary classification models.",
            "Netflix EDA output informs content acquisition, regional localization, and genre investment decisions.",
            "Shared Foundation: Rigorous data understanding, reproducible scripts, and clear 'What does this mean?' business framing.",
        ],
    )

    prs.save(OUTPUT_PPTX)
    print(f"Saved 5-slide comparison deck to: {OUTPUT_PPTX}")


if __name__ == "__main__":
    main()
