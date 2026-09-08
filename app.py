from flask import Flask, render_template, request
from database import get_connection

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        startup_name = request.form["project_name"]
        industry = request.form["industry"]
        business_model = request.form["business_model"]
        target_market = request.form["target_market"]
        budget = request.form["budget"]
        description = request.form["description"]

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO projects
                (startup_name, industry, business_model, target_market, budget, project_description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                startup_name,
                industry,
                business_model,
                target_market,
                budget,
                description
            ))

            conn.commit()

            message = "Project submitted successfully!"

            cursor.close()
            conn.close()

        except Exception as e:
            message = f"Database error: {e}"


    # Fetch all submitted projects
    projects = []

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT startup_name,
                   industry,
                   business_model,
                   target_market,
                   budget,
                   project_description
            FROM projects
            ORDER BY startup_name
        """)

        projects = cursor.fetchall()

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error loading projects:", e)


    return render_template(
        "dashboard.html",
        message=message,
        projects=projects
    )


if __name__ == "__main__":
    app.run(debug=True)