import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# 2. Clean data (remove top 2.5% and bottom 2.5%)
lower = df["value"].quantile(0.025)
upper = df["value"].quantile(0.975)
df = df[(df["value"] >= lower) & (df["value"] <= upper)]


# 3. Line Plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df["value"], color="red")

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    plt.tight_layout()
    return fig


# 4. Bar Plot
def draw_bar_plot():
    # Prepare data
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Group by year and month
    df_grouped = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Plot
    fig = df_grouped.plot(kind="bar", figsize=(12, 8)).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Month names for legend
    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    plt.legend(month_names, title="Months")

    plt.tight_layout()
    return fig


# 5. Box Plot
def draw_box_plot():
    df_box = df.copy()

    # Prepare data
    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.strftime("%b")
    df_box["month_num"] = df_box.index.month

    # Sort months
    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Year-wise box plot
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    plt.tight_layout()
    return fig