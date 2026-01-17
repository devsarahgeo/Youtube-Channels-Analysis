# 📺 Youtube Channels Analysis

## 🧭 Executive Summary
<p>
This project analyzes YouTube channel performance to identify data-driven strategies for increasing views, engagement, and long-term growth.
Using a modern analytics stack - <strong>Snowflake, dbt, Airflow, and Power BI</strong>, raw YouTube data was transformed into scalable,
analysis-ready datasets and visualized to uncover actionable insights around content timing, topics, and engagement behavior.
</p>

<p>
The goal is to help data creators understand <strong>what to post, when to post, and which topics drive traction</strong>,
enabling smarter content decisions from day one.
</p>

### 💼 Business Problem
<p>
With increasing competition on YouTube, intuition alone is no longer enough for consistent growth.
Creators need reliable analytics to understand audience behavior and content performance.
</p>

<ul>
  <li>Identify optimal <strong>upload days and times</strong> to maximize views</li>
  <li>Analyze <strong>topic-level engagement rates</strong> (e.g., SQL, Power BI, Data Engineering)</li>
  <li>Understand how <strong>launch timing</strong> affect performance</li>
  <li>Build an <strong>automated and scalable analytics pipeline</strong> for ongoing reporting</li>
</ul>

---

## ⚙️ Methodology 

<h3>1. Data Ingestion & Orchestration (Apache Airflow)</h3>

<h3> Dataset Used:</h3> 
Youtube Live Api considering top 120 channels high performing videos with subscriber count greater than or equal to 10k
<br>-----
<ul>
  <li>Built automated <strong>Airflow DAGs</strong> to ingest YouTube metadata</li>
  <li>Scheduled workflows for reliable and repeatable data refreshes</li>
  <li>Loaded raw data directly into <strong>Snowflake</strong></li>
</ul>

<h3>2. Data Warehousing (Snowflake)</h3>
<ul>
  <li>Centralized raw and transformed data in Snowflake</li>
  <li>Designed schemas optimized for analytical querying</li>
</ul>

<h3>3. Data Transformation (dbt)</h3>
<ul>
  <li>Used <strong>dbt</strong> to clean, standardize, and model YouTube data</li>
  <li>Created analytics-ready <strong>fact/dimension tables and marts</strong></li>
  <!-- <li>Engineered key metrics:
    <ul>
      <li>Average views</li>
      <li>Engagement rate (<em>(likes + comments) / views</em>)</li>
      <li>Upload hour and day of week</li>
      <li>Video duration buckets</li>
    </ul>
  </li>
  <li>Implemented dbt tests to ensure data quality</li> -->
</ul>

<h3>4. Visualization & Insights (Power BI)</h3>
<ul>
  <li>Built interactive <strong>Power BI dashboards</strong></li>
  <li>Line and bar charts highlighting performance trends</li>
  <li>Topic-level comparisons to identify high-performing content areas</li>
  <li> Used DAX queries where needed (eg - to create buckets for times of day like morning, afternoon etc)</li>
</ul>
---

## 🧠 Skills & Tech Stack
<ul>
  <li><strong>Snowflake</strong> – Cloud data warehousing</li>
  <li><strong>dbt</strong> – Data modeling and transformation</li>
  <li><strong>Apache Airflow</strong> – Workflow orchestration</li>
  <li><strong>Visual Studio Code</strong> – Central development environment</li>
  <li><strong>Power BI</strong> – Data visualization and storytelling</li>
  <li><strong>SQL</strong> – Analytical querying</li>
  <li><strong>Analytics Engineering</strong> – End-to-end pipeline development</li>
  <li>Draw.io for achitecture diagram</li>
</ul>

---

## 📈 Results

Power BI Report Snapshot:
<img width="1384" height="775" alt="Screenshot 2026-01-17 at 10 43 28 AM" src="https://github.com/user-attachments/assets/17038671-9b92-42ff-9fc5-4d86e83ef561" />
<img width="1384" height="781" alt="Screenshot 2026-01-17 at 10 43 49 AM" src="https://github.com/user-attachments/assets/c5feafda-a71a-47af-aae2-6f6d086994d7" />


<h3>Architecture Diagram:</h3>
<img width="1601" height="741" alt="YouTube Channel Analysis" src="New YouTube Channel Analysis.svg" />

<ul>
  <li>Upload timing significantly impacts performance, with specific <strong>days and afternoon time windows</strong> showing higher median views</li>
  <li>Technical topics such as <strong>SQL and Power BI</strong> achieved higher engagement rates</li>
  <li>Channels with fewer but <strong>strategically timed uploads</strong> often outperformed high-frequency uploaders</li>
  <li>Video duration and description length showed weak correlations, indicating <strong>content quality outweighs length</strong></li>
</ul>

<b>Conclusion:</b>
Early-stage data related YouTube channels gain faster traction by focusing on high-engagement, beginner-friendly topics such as SQL, and job-related content, while scheduling uploads early in the week-especially Monday afternoons. More advanced topics should be introduced later to sustain long-term growth once the channel has established an engaged audience.

## 📂 Deliverables
<ul>
  <li><strong>Power BI Dashboard</strong> - Interactive exploration of YouTube performance metrics</li>
  <li><strong>dbt Models</strong> - Clean, tested analytics-ready datasets</li>
  <li><strong>Airflow DAGs</strong> – Automated ingestion workflows</li>
  <li><strong>Snowflake Tables</strong> – Scalable analytical storage</li>
</ul>

## 📂 Impact
<p>
This project demonstrates how a modern analytics stack can transform raw YouTube data into
<strong>actionable growth insights</strong>, enabling data creators to make informed decisions around
content strategy, timing, and topic selection.
</p>


